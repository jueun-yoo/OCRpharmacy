from django.shortcuts import render, get_object_or_404, redirect
from .models import Nutrient, Supplement, RecommendedIntake, Synonym
from .forms import SupplementForm, ImageUploadForm, OCRResultEditForm
import cv2
import uuid
import json
import time
import requests
from PIL import Image, ImageDraw
from io import BytesIO  # io 모듈에서 BytesIO를 import 합니다.

# Create your views here.
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






############################################OCR관련 view#######################################################################################
# 영양제 추가하는 함수
def add_supplement(request):
    if request.method == 'POST':
        form = SupplementForm(request.POST)
        if form.is_valid():
            supplement = form.save(commit=False)  # 데이터베이스에 저장되지 않은 모델 객체 생성
            supplement.user_id = request.user.id  # 현재 로그인한 유저의 ID를 할당
            supplement.name = form.cleaned_data['name']  # 사용자가 입력한 영양제 이름을 할당
            supplement.save()  # 실제로 데이터베이스에 저장
            return redirect('upload_image_page.html')  # 영양제 추가 후 이미지 업로드 페이지로 이동
    else:
        form = SupplementForm()

    return render(request, 'add_supplement.html', {'form': form})

# 이미지 업로드 및 전처리 함수
def upload_image_and_preprocess(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            image_file = request.FILES['image']

            ####전처리#####
            # 이미지 로드
            img = cv2.imread(image_file.temporary_file_path())
            # 그레이 스케일 변환
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 가우시안 블러 적용 
            img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
            # Adaptive 이진화 적용
            img_adaptive = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=3, C=3)
            # 노이즈 제거
            img_denoise = cv2.fastNlMeansDenoising(img_adaptive)
            # 색상 반전
            img_inverted = cv2.bitwise_not(img_denoise)

            # 전처리된 이미지를 세션에 저장
            request.session['preprocessed_image'] = img_inverted

            # HTTP 응답을 반환하거나 다른 페이지로 리디렉션할 수 있습니다
            return render(request, 'result_page.html')

    else:
        form = ImageUploadForm()

    return render(request, 'upload_image_page.html', {'form': form})

# OCR함수
def perform_ocr_and_save(request):
    # 세션에서 전처리된 이미지 가져오기
    preprocessed_image = request.session.get('preprocessed_image')
    # 원본 이미지 가져오기 (Image 객체로 변환)
    original_image = Image.open(request.FILES['image'].temporary_file_path())
    # 전처리 후, OCR작업
    api_url = 'https://3g69izliq5.apigw.ntruss.com/custom/v1/23692/83af5a7f71fe00ce5a40c5be9622db4c5114ba6702fdc14ddb1b4b007e5ca726/general'
    secret_key = 'UFRkQlFOSlhNUW5QS0FRamdtTnpOTWpjbmxGQ2JUek8='
    image_file = preprocessed_image  # 이미지 파일 경로임 추후 수정해야됨!!!!!
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
        # 결과를 이미지에 그리기
        draw = ImageDraw.Draw(original_image)
        extracted_text = []
        start_extracting = False  # '1일'이 발견된 이후부터 추출 시작
        for item in output_json['images'][0]['fields']:
            bounding_box = item['boundingPoly']
            vertices = bounding_box['vertices']
            coordinates = [(v['x'], v['y']) for v in vertices]
            # 텍스트 영역에 박스 그리기 (녹색)
            draw.polygon(coordinates, outline='green')
            # 텍스트 그리기
            text = item['inferText']
            if '1일' in text:
                start_extracting = True
            if start_extracting:
                extracted_text.append(text)
        extracted_text_str = ' '.join(extracted_text)  # 공백을 이용하여 하나의 줄로 합침
        extracted_text_str = extracted_text_str.replace(" ", "")  # Remove all spaces from the text
        print('추출된 텍스트:\n', extracted_text_str)  # 추출된 텍스트 확인
        import re
        # 쉼표로 분리하여 리스트로 저장
        lines = extracted_text_str.split(',')
        print(lines)

        nutrient_mapping = {
            "열량": "열량",
            "단백질": "단백질",
            "식이섬유": "식이섬유",
            "수분": "수분",
            "비타민A": "비타민A",
            "비타민D": "비타민D",
            "비타민E": "비타민E",
            "비타민K": "비타민K",
            "비타민C": "비타민C",
            "티아민": "티아민",
            "리보플라민": "리보플라민",
            "나이아신": "나이아신",
            "비타민B6": "비타민B6",
            "엽산": "엽산",
            "비타민B12": "비타민B12",
            "판토텐산": "판토텐산",
            "비오틴": "비오틴",
            "칼슘": "칼슘",
            "인": "인",
            "나트륨": "나트륨",
            "염소": "염소",
            "칼륨": "칼륨",
            "마그네슘": "마그네슘",
            "철": "철",
            "아연": "아연",
            "구리": "구리",
            "불소": "불소",
            "망간": "망간",
            "요오드": "요오드",
            "셀레늄": "셀레늄",
            "몰데브덴": "몰데브덴"
            # 필요한 영양소 매핑을 여기에 추가하세요, 외국 영양제면 나중에 ex)"protien": "단백질" 이런식으로 추가하면 될듯?
            }

        nutrient_data = {}

        for line in lines:
            for nutrient_name, nutrient_key in nutrient_mapping.items():
                if nutrient_name in line:
                    if nutrient_name == "열량":
                        value_start = line.find(nutrient_name) + len(nutrient_name)
                        value_end = line.find("kcal", value_start) + len("kcal") + 1
                    else:
                        value_start = line.find(nutrient_name) + len(nutrient_name)
                        value_end = line.find("g", value_start) + 1
                    
                    nutrient_value = line[value_start:value_end].strip()  # Remove any extra spaces
                    nutrient_data[nutrient_key] = nutrient_value

        # 세션에 데이터 저장
        request.session['ocr_result'] = nutrient_data

        # 이미지를 BytesIO 객체에 저장하여 사용자에게 보여줌
        image_io = BytesIO()
        original_image.save(image_io, format='JPEG')
        image_io.seek(0)

        # HTTP 응답을 반환하거나 다른 페이지로 리디렉션할 수 있습니다.
        return render(request, 'result_page.html', {'ocr_result': nutrient_data, 'image_data': image_io})

    else:
        print('API 요청에 실패했습니다. 상태 코드:', response.status_code)
        return render(request, 'result_page.html', {'ocr_result': '', 'image_data': None})

# OCR 결과 수정 함수
def edit_ocr_result(request):
    ocr_result = request.session.get('ocr_result', {})
    edited_ocr_result = request.session.get('edited_ocr_result', {})

    if request.method == 'POST':
        form = OCRResultEditForm(request.POST)
        if form.is_valid():
            edited_ocr_result = form.cleaned_data['edited_ocr_result']
            request.session['edited_ocr_result'] = edited_ocr_result
            # 기존의 OCR 결과 업데이트
            ocr_result.update(edited_ocr_result)
            request.session['ocr_result'] = ocr_result
            return redirect('edit_ocr_result')  # 수정 후 다시 수정 페이지로 리디렉션
    else:
        form = OCRResultEditForm(initial={'edited_ocr_result': edited_ocr_result})

    return render(request, 'edit_ocr_result.html', {'form': form, 'edited_ocr_result': edited_ocr_result})