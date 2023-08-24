from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from .models import Supplement, Nutrient, UserTotalIntake
from .models import Supplement, SupplementNutrient, RecommendedNutrient, Interaction, Synonym
import cv2
import uuid
import json
import time
import requests
import sqlite3
from PIL import Image, ImageDraw
from io import BytesIO  # io 모듈에서 BytesIO를 import 합니다.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.base import ContentFile
import base64
import numpy as np
import random

# Create your views here.
# 영양소 상세 보기
def nutrient_detail(request, nutrient_name):
    nutrient = get_object_or_404(Nutrient, name=nutrient_name)
    return render(request, 'supplements/nutrient_detail.html', {'nutrient': nutrient})

def supplement_detail(request, supplement_id):
    supplement = get_object_or_404(Supplement, id=supplement_id)
    user = request.user

    supplement_nutrients = {sn.nutrient.name: sn.dosage for sn in SupplementNutrient.objects.filter(supplement=supplement)}
    recommended_nutrients = {rn.nutrient.name: rn.dosage for rn in RecommendedNutrient.objects.filter(recommended_intake=user.recommended)}
    limit_nutrients = {qn.nutrient.name: qn.limit for qn in RecommendedNutrient.objects.filter(recommended_intake=user.recommended)}

    over_nutrients = {}
    under_nutrients = {}
    remaining_nutrients = {}
    for nutrient, dosage in supplement_nutrients.items():
        recommended_dosage = recommended_nutrients.get(nutrient)
        limit_dosage = limit_nutrients.get(nutrient)
        if recommended_dosage:
            percentage = (dosage / recommended_dosage) * 100
            if limit_dosage and limit_dosage < dosage:
                over_nutrients[nutrient] = percentage
            elif percentage < 50:
                under_nutrients[nutrient] = percentage
            else:
                remaining_nutrients[nutrient] = percentage 

    # 상호작용 객체를 담을 빈 리스트를 만듭니다.
    interactions = []

    # 영양제의 SupplementNutrient 객체들 중에서 용량이 0이 아닌 것만 선택합니다.
    supplement_nutrients_with_dosage = [sup_nut for sup_nut in SupplementNutrient.objects.filter(supplement=supplement) if sup_nut.dosage > 0]

    # 모든 상호작용 객체를 순회합니다.
    all_interactions = Interaction.objects.all()
    for interaction in all_interactions:
        # 상호작용의 두 성분이 모두 영양제에 포함되어 있고, 용량이 0이 아닌지 확인합니다.
        if interaction.nutrient1 in [sup_nut.nutrient for sup_nut in supplement_nutrients_with_dosage] and interaction.nutrient2 in [sup_nut.nutrient for sup_nut in supplement_nutrients_with_dosage]:
            # 두 성분이 모두 포함되어 있고 용량이 0이 아니라면 interactions 리스트에 추가합니다.
            interactions.append(interaction)

    return render(request, 'supplements/supplement_detail.html', {
    'supplement': supplement,
    'over_nutrients': over_nutrients,
    'under_nutrients': under_nutrients,
    'remaining_nutrients': remaining_nutrients,
    'interactions': interactions
})

def delete_supplement(request, supplement_id):
    supplement = get_object_or_404(Supplement, id=supplement_id)
    supplement.delete()
    return redirect('user:index')

def upload_image(request):
    if request.method == 'POST':
        # 'file' 키가 있는지 확인
        image_file = request.FILES.get('file')
        if not image_file:
            return JsonResponse({'success': False, 'message': '파일이 없습니다.'})
        
        # 파일을 읽어 base64로 인코딩, 세션에 저장
        image_data = base64.b64encode(image_file.read())
        request.session['uploaded_image_base64'] = image_data.decode('utf-8')

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'message': 'POST 요청이 아닙니다.'})

###############정보추출함수 내놔..
def extract_info_from_image(image_np):
    _, image_file = cv2.imencode('.jpg', image_np)
    image_file_buffer = BytesIO(image_file)


    api_url = 'https://3g69izliq5.apigw.ntruss.com/custom/v1/23692/83af5a7f71fe00ce5a40c5be9622db4c5114ba6702fdc14ddb1b4b007e5ca726/general'
    secret_key = 'UFRkQlFOSlhNUW5QS0FRamdtTnpOTWpjbmxGQ2JUek8='
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
        ('file', ('demo.jpg', image_file_buffer, 'image/jpeg'))  # 파일 대신 바이트 스트림 객체를 전달
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
        processed_nutrients = set()
        # Extracted lines from OCR
        for line in lines:
            for nutrient_name_db, unit in nutrient_data_db:  # unit도 가져온 데이터에서 사용
                if nutrient_name_db in line and nutrient_name_db not in processed_nutrients:
                    if nutrient_name_db == "열량":
                        value_start = line.find(nutrient_name_db) + len(nutrient_name_db)
                        value_end = line.find("kcal", value_start) + len("kcal") + 1
                    else:
                        value_start = line.find(nutrient_name_db) + len(nutrient_name_db)
                        value_end = line.find("g", value_start) + 1
                    nutrient_value = line[value_start:value_end].strip()
                    if not any(char.isdigit() for char in nutrient_value):
                        continue
                    # 추출한 값에서 단위를 제외한 숫자만 추출하여 저장
                    nutrient_value = ''.join([c for c in nutrient_value if c.isdigit() or c == '.'])
                    if nutrient_value:  # 빈 값을 방지하기 위해 확인
                        nutrient_value = float(nutrient_value)  # 문자열을 숫자로 변환
                    else:
                        nutrient_value = 0.0
                    processed_nutrients.add(nutrient_name_db)
                    # 영양소 정보를 딕셔너리로 구성하여 리스트에 추가
                    nutrient_info = {
                        'name': nutrient_name_db,
                        'dosage': nutrient_value,
                        'unit': unit  # 데이터베이스에서 가져온 unit 사용
                    }
                    extracted_info.append(nutrient_info)
    return extracted_info

def process_image(request):
    # 세션에서 이미지 데이터 가져오기
    uploaded_image_base64 = request.session.get('uploaded_image_base64')
    if uploaded_image_base64:
        # base64 데이터를 이미지로 변환
        image_data = base64.b64decode(uploaded_image_base64)
        image_data_buffer = BytesIO(image_data)
        image_data_np = np.frombuffer(image_data_buffer.read(), np.uint8)
        img = cv2.imdecode(image_data_np, cv2.IMREAD_COLOR)
        
        #이미지처리 코드

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
        
        # POST 데이터에서 영양제 이름을 가져옵니다.
        supplement_name = request.POST.get('supplement_name', '')
        

        # 이미지를 파일로 저장하지 않고, invert 처리한 이미지를 직접 추출 함수에 전달합니다.
        extracted_info = extract_info_from_image(img_inverted)


        info = {
                'name': supplement_name,
                'nutrients': extracted_info
                }

        # 추출된 정보를 세션에 저장
        request.session['info'] = info
        request.session['supplement_name'] = supplement_name

        # 세션에서 이미지 데이터 삭제
        del request.session['uploaded_image_base64']

        return render(request, 'supplements/preview.html', {'info': info})  # save_info URL로 리다이렉트
    else:
        # 오류 처리 (예: 이미지가 세션에 없음)
        return JsonResponse({'success': False, 'error': 'Image not found in session'})

from django.shortcuts import render, redirect
from .models import Supplement, SupplementNutrient, Nutrient
from django.contrib import messages
import logging


def save_info(request):
    if request.method == 'POST':
        print(request.POST)
        supplement_name = request.POST.get('supplement_name')        

        # 기존 보충제를 가져옵니다.
        supplement = Supplement(name=supplement_name, user=request.user)
        supplement.save()

        # nutrients 정보를 동적으로 처리합니다.
        nutrients_info = []
        i = 0
        while True:
            nutrient_name = request.POST.get(f'nutrients[{i}][name]')
            if nutrient_name is None:
                break
            dosage = float(request.POST.get(f'nutrients[{i}][dosage]'))
            nutrients_info.append((nutrient_name, dosage))
            i += 1
        
        new_nutrients_info = []
        j = 0
        while True:
            new_nutrient_name = request.POST.get(f'new_nutrients[{j}][name]')
            if new_nutrient_name is None:
                break
            new_dosage = float(request.POST.get(f'new_nutrients[{j}][dosage]'))
            new_nutrients_info.append((new_nutrient_name, new_dosage))
            j += 1

        for nutrient_name, dosage in nutrients_info:
            try:
                nutrient = Nutrient.objects.get(name=nutrient_name)
                unit = nutrient.unit
            except Nutrient.DoesNotExist:
                continue

            supplement_nutrient = SupplementNutrient(nutrient=nutrient, supplement=supplement, dosage=dosage, unit=unit)
            supplement_nutrient.save()
            
        for new_nutrient_name, new_dosage in new_nutrients_info:
            try:
                nutrient = Nutrient.objects.get(name=new_nutrient_name)
                unit = nutrient.unit
            except Nutrient.DoesNotExist:
                continue

            supplement_nutrient = SupplementNutrient(nutrient=nutrient, supplement=supplement, dosage=new_dosage, unit=unit)
            supplement_nutrient.save()

        return redirect('user:index')

    return redirect('error')