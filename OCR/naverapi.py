import uuid
import json
import time
import requests
from PIL import Image, ImageDraw, ImageFont

api_url = 'https://3g69izliq5.apigw.ntruss.com/custom/v1/23692/83af5a7f71fe00ce5a40c5be9622db4c5114ba6702fdc14ddb1b4b007e5ca726/general'
secret_key = 'UFRkQlFOSlhNUW5QS0FRamdtTnpOTWpjbmxGQ2JUek8='
image_file = 'result1.jpg' #이미지 파일 경로임 추우 수정해야됨!!!!!

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
    ('file', open(image_file,'rb'))
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

    # 이미지 생성
    image = Image.open(image_file)
    draw = ImageDraw.Draw(image)

    # 결과를 이미지에 그리고 텍스트 저장 및 출력
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

    # 이미지 저장
    output_image_file = 'clova_image.jpg'
    image.save(output_image_file)
    print('이미지 저장 완료:', output_image_file)

    # 추출된 텍스트 저장
    output_text_file = 'clova_text.txt'
    with open(output_text_file, 'w', encoding='utf-8') as f:
        extracted_text_str = ' '.join(extracted_text)  # 공백을 이용하여 하나의 줄로 합침
        f.write(extracted_text_str)
        print('텍스트 저장 완료:', output_text_file)
        print('저장된 텍스트:\n', extracted_text_str)
else:
    print('API 요청에 실패했습니다. 상태 코드:', response.status_code)