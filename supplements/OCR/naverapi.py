import uuid
import json
import time
import requests
import sqlite3
from PIL import Image, ImageDraw, ImageFont

#영양제,영양소,함량 추가 함수
def add_dosage(dosage, nutrient_id, supplement_id):
    sql = "INSERT INTO supplements_supplementnutrient (dosage, nutrient_id, supplement_id) VALUES (?, ?, ?)"
    cursor.execute(sql, (dosage, nutrient_id, supplement_id))
    conn.commit()

api_url = 'https://3g69izliq5.apigw.ntruss.com/custom/v1/23692/83af5a7f71fe00ce5a40c5be9622db4c5114ba6702fdc14ddb1b4b007e5ca726/general'
secret_key = 'UFRkQlFOSlhNUW5QS0FRamdtTnpOTWpjbmxGQ2JUek8='
image_file =  r"C:\Microsoft VS Code\2023DNA\OCR\55.jpg" # 이미지 파일 경로임 추후 수정해야됨!!!!!
original_image = Image.open(r"C:\Microsoft VS Code\2023DNA\OCR\55.jpg")
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
    nutrient_list = []
    processed_nutrients = set() # Processed nutrients

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
                nutrient_list.append(nutrient_info)

    # 딕셔너리 출력
    print("영양소 정보 딕셔너리:", nutrient_list)

    
    # 이미지 저장
    output_image_file = r"C:\Microsoft VS Code\2023DNA\OCR\clova_image.jpg"
    original_image.save(output_image_file)
    print('\n이미지 저장 완료:', output_image_file)
"""
    # 추출된 텍스트 저장
    output_text_file = r"C:\Microsoft VS Code\2023DNA\OCR\clova_text.txt"
    with open(output_text_file, 'w', encoding='utf-8') as f:
        nutrient_data_str = json.dumps(nutrient_data, ensure_ascii=False, indent=4)
        f.write(nutrient_data_str)
        print('텍스트 저장 완료:', output_text_file)
        print('저장된 텍스트:\n', nutrient_data_str)
"""