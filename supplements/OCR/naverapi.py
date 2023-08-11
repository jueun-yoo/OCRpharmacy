import uuid
import json
import time
import requests
from PIL import Image, ImageDraw, ImageFont

api_url = 'https://3g69izliq5.apigw.ntruss.com/custom/v1/23692/83af5a7f71fe00ce5a40c5be9622db4c5114ba6702fdc14ddb1b4b007e5ca726/general'
secret_key = 'UFRkQlFOSlhNUW5QS0FRamdtTnpOTWpjbmxGQ2JUek8='
image_file =  r"C:\Microsoft VS Code\2023DNA\OCR\result1.jpg" # 이미지 파일 경로임 추후 수정해야됨!!!!!
original_image = Image.open(r"C:\Microsoft VS Code\2023DNA\OCR\1.jpg")
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
        # 필요한 영양소 매핑을 여기에 추가하세요
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

    print("영양소 데이터:", nutrient_data)

    # 이미지 저장
    output_image_file = r"C:\Microsoft VS Code\2023DNA\OCR\clova_image.jpg"
    original_image.save(output_image_file)
    print('\n이미지 저장 완료:', output_image_file)

    # 추출된 텍스트 저장
    output_text_file = r"C:\Microsoft VS Code\2023DNA\OCR\clova_text.txt"
    with open(output_text_file, 'w', encoding='utf-8') as f:
        nutrient_data_str = json.dumps(nutrient_data, ensure_ascii=False, indent=4)
        f.write(nutrient_data_str)
        print('텍스트 저장 완료:', output_text_file)
        print('저장된 텍스트:\n', nutrient_data_str)
else:
    print('API 요청에 실패했습니다. 상태 코드:', response.status_code)