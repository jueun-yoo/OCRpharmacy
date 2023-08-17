from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from .models import Supplement, Nutrient
from .models import Supplement, SupplementNutrient, RecommendedNutrient, Interaction
import cv2
import uuid
import json
import time
import requests
import sqlite3
from PIL import Image, ImageDraw
from io import BytesIO  # io 모듈에서 BytesIO를 import 합니다.

""" # Create your views here.
# 영양소 상세 보기
def nutrient_detail(request, nutrient_id):
    nutrient = get_object_or_404(Nutrient, pk=nutrient_id)
    return render(request, 'nutrient_detail.html', {'nutrient': nutrient})

# 영양소 상세 보기와 동의어 함께 보기
def nutrient_detail_with_synonyms(request, nutrient_id):
    nutrient = get_object_or_404(Nutrient, pk=nutrient_id)

    # OCR에서 가져온 영양소 표현 (예시로 "비타민B1"로 가정)
    ocr_expression = "비타민B1"

    # OCR로부터 가져온 표현이 "비타민B1"인 경우, "티아민"으로 변경
    if ocr_expression == "비타민B1":
        ocr_expression = "티아민"

    return render(request, 'nutrient_detail_with_synonyms.html', {'nutrient': nutrient, 'ocr_expression': ocr_expression})
 """

def supplement_detail(request, supplement_id):
    supplement = get_object_or_404(Supplement, id=supplement_id)
    user = request.user

    supplement_nutrients = {sn.nutrient.name: sn.dosage for sn in SupplementNutrient.objects.filter(supplement=supplement)}
    recommended_nutrients = {rn.nutrient.name: rn.dosage for rn in RecommendedNutrient.objects.filter(recommended_intake=user.recommended)}


    nutrient_percentages = {}
    for nutrient, dosage in supplement_nutrients.items():
        recommended_dosage = recommended_nutrients.get(nutrient)
        if recommended_dosage:
            percentage = (dosage / recommended_dosage) * 100
            nutrient_percentages[nutrient] = percentage


    interactions = Interaction.objects.filter(nutrient1__in=supplement.nutrients.all(), nutrient2__in=supplement.nutrients.all())

    return render(request, 'supplements/supplement_detail.html', {
        'supplement': supplement,
        'nutrient_percentages': nutrient_percentages,
        'interactions': interactions
    })

def upload_image(request):
    if request.method == 'POST':
        image_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        uploaded_file_url = fs.url(filename)

        # 세션에 임시 이미지 URL 저장
        request.session['uploaded_file_url'] = uploaded_file_url

        return redirect('supplements:process_image')

###############정보추출함수 내놔..
def extract_info_from_image(img_inverted):
    # 전처리 후, OCR작업
    api_url = 'https://3g69izliq5.apigw.ntruss.com/custom/v1/23692/83af5a7f71fe00ce5a40c5be9622db4c5114ba6702fdc14ddb1b4b007e5ca726/general'
    secret_key = 'UFRkQlFOSlhNUW5QS0FRamdtTnpOTWpjbmxGQ2JUek8='
    image_file = img_inverted  # 이미지 파일 경로임 추후 수정해야됨!!!!!
    # 이미지 파일을 API에 전송하기 위한 요청 데이터 생성
    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }
    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [
        ('file', open(image_file, 'rb'))
    ]
    headers = {
        'X-OCR-SECRET': secret_key
    }
    # API 요청 보내기
    response = requests.post(api_url, headers=headers, data=payload, files=files)
    # 응답 결과 확인
    if response.status_code == 200:
        output_json = response.json()
        print(output_json)
        extracted_text = []
        start_extracting = False  # '1일'이 발견된 이후부터 추출 시작
        for item in output_json['images'][0]['fields']:
            bounding_box = item['boundingPoly']
            vertices = bounding_box['vertices']
            coordinates = [(v['x'], v['y']) for v in vertices]
            # 텍스트 그리기
            text = item['inferText']
            if '1일' in text:
                start_extracting = True
            if start_extracting:
                extracted_text.append(text)
        extracted_text_str = ' '.join(extracted_text)  # 공백을 이용하여 하나의 줄로 합침
        extracted_text_str = extracted_text_str.replace(" ", "")  # Remove all spaces from the text
        print('추출된 텍스트:\n', extracted_text_str)  # 추출된 텍스트 확인
        # 쉼표로 분리하여 리스트로 저장
        lines = extracted_text_str.split(',')
        print(lines)
        # SQLite 데이터베이스에 연결
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('SELECT name, unit FROM supplements_nutrient')  # unit도 가져오도록 수정
        nutrient_data_db = cursor.fetchall()
        # 연결 종료
        conn.close()
        # 영양소 정보를 저장할 리스트 초기화
        extracted_info = []
        # Extracted lines from OCR
        for line in lines:
            for nutrient_name_db, unit in nutrient_data_db:  # unit도 가져온 데이터에서 사용
                if nutrient_name_db in line:
                    if nutrient_name_db == "열량":
                        value_start = line.find(nutrient_name_db) + len(nutrient_name_db)
                        value_end = line.find("kcal", value_start) + len("kcal") + 1
                    else:
                        value_start = line.find(nutrient_name_db) + len(nutrient_name_db)
                        value_end = line.find("g", value_start) + 1
                    nutrient_value = line[value_start:value_end].strip()
                    # 추출한 값에서 단위를 제외한 숫자만 추출하여 저장
                    nutrient_value = ''.join([c for c in nutrient_value if c.isdigit() or c == '.'])
                    if nutrient_value:  # 빈 값을 방지하기 위해 확인
                        nutrient_value = float(nutrient_value)  # 문자열을 숫자로 변환
                    else:
                        nutrient_value = 0.0
                    # 영양소 정보를 딕셔너리로 구성하여 리스트에 추가
                    nutrient_info = {
                        'name': nutrient_name_db,
                        'dosage': nutrient_value,
                        'unit': unit  # 데이터베이스에서 가져온 unit 사용
                    }
                    extracted_info.append(nutrient_info)
    return extracted_info

def process_image(request):
    uploaded_file_url = request.session.get('uploaded_file_url')
    #전처리#
    image_file = request.FILES['image']
    img = cv2.imread(image_file.temporary_file_path())
    # 그레이 스케일 변환#
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 가우시안 블러 적용 
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
    # Adaptive 이진화 적용
    img_adaptive = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=3, C=3)
    # 노이즈 제거
    img_denoise = cv2.fastNlMeansDenoising(img_adaptive)
    # 색상 반전
    img_inverted = cv2.bitwise_not(img_denoise)
    # 이미지에서 필요한 정보 추출 (정보추출 함수 필요)
    extracted_info = extract_info_from_image(img_inverted)

    # 추출된 정보를 세션에 저장
    request.session['extracted_info'] = extracted_info

    return render(request, 'preview.html', {'info': extracted_info})

from django.shortcuts import render, redirect
from .models import Supplement, SupplementNutrient, Nutrient

def save_info(request):
    if request.method == 'POST':
        # 세션에서 추출된 정보를 가져옵니다.
        extracted_info = request.session.get('extracted_info')

        # Supplement 객체를 생성합니다.
        supplement = Supplement(name=extracted_info['name'], user=request.user)
        supplement.save()

        # 각 영양소 정보를 저장합니다.
        for nutrient_info in extracted_info['nutrients']:
            nutrient_name = nutrient_info['name']
            dosage = nutrient_info['dosage']
            unit = nutrient_info['unit']

            # 영양소를 찾거나 새로 생성합니다.
            nutrient, created = Nutrient.objects.get_or_create(name=nutrient_name)

            # SupplementNutrient 객체를 생성하고 연결합니다.
            supplement_nutrient = SupplementNutrient(nutrient=nutrient, supplement=supplement, dosage=dosage, unit=unit)
            supplement_nutrient.save()

        return redirect('success')

    return redirect('error')
