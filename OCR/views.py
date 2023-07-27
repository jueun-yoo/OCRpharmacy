from django.shortcuts import render
from .forms import ImageUploadForm
import cv2
import uuid
import json
import time
import requests
from PIL import Image, ImageDraw
from io import BytesIO  # io 모듈에서 BytesIO를 import 합니다.

# 문자열 파싱하여 영양소와 용량 정보 추출하는 함수
# 예: 입력 문자열 "칼륨:10g, 비타민C:10mg" => {"칼륨": "10g", "비타민C": "10mg"}
def parse_nutrient_info(text):
    nutrient_info = {}
    parts = text.split(",")  # ,로 분리리
    for part in parts:
        nutrient, amount = part.split(":")  # 영양소와 용량 정보 추출
        nutrient_info[nutrient.strip()] = amount.strip()
    return nutrient_info

# 이미지 전처리 함수
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
            # 빛 반사-CLAHE 객체 생성
            clahe = cv2.createCLAHE(clipLimit=1, tileGridSize=(4, 4))
            # 빛 반사-CLAHE 적용
            img_clahe = clahe.apply(img_gray)
            # 가우시안 블러 적용 
            img_blur = cv2.GaussianBlur(img_clahe, (3, 3), 0)
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

        # 추출된 텍스트를 세션에 저장합니다.
        extracted_text_str = ' '.join(extracted_text)
        request.session['ocr_result'] = extracted_text_str

        # 이미지를 BytesIO 객체에 저장하여 사용자에게 보여줌
        image_io = BytesIO()
        original_image.save(image_io, format='JPEG')
        image_io.seek(0)

        # HTTP 응답을 반환하거나 다른 페이지로 리디렉션할 수 있습니다.
        return render(request, 'result_page.html', {'ocr_result': extracted_text_str, 'image_data': image_io})

    else:
        print('API 요청에 실패했습니다. 상태 코드:', response.status_code)
        return render(request, 'result_page.html', {'ocr_result': '', 'image_data': None})

# OCR 결과 수정 함수
def edit_ocr_result(request):
    # POST 요청을 처리하여 수정된 결과를 세션에 저장합니다.
    if request.method == 'POST':
        edited_ocr_result = request.POST.get('edited_ocr_result')
        request.session['ocr_result'] = edited_ocr_result

    # 세션에서 OCR 결과를 가져옵니다.
    ocr_result = request.session.get('ocr_result', '')

    return render(request, 'result_page.html', {'ocr_result': ocr_result})