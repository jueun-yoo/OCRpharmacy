import sqlite3

# 데이터베이스에 연결
conn = sqlite3.connect('db.sqlite3')  # 파일명은 실제 파일의 경로를 써야 합니다.

# 커서 생성
cursor = conn.cursor()

# 데이터 추가
def add_supplements_nutrient(name, details):
    sql = "INSERT INTO supplements_nutrient (name, details) VALUES (?, ?)"
    cursor.execute(sql, (name, details))
    conn.commit()

# 데이터 추가 예시
add_supplements_nutrient("열량", ".")
add_supplements_nutrient("단백질", ".")
add_supplements_nutrient("식이섬유", ".")
add_supplements_nutrient("수분", ".")
add_supplements_nutrient("비타민A", ".")
add_supplements_nutrient("비타민D", ".")
add_supplements_nutrient("비타민E", ".")
add_supplements_nutrient("비타민K", ".")
add_supplements_nutrient("비타민C", ".")
add_supplements_nutrient("티아민", ".")
add_supplements_nutrient("리보플라민", ".")
add_supplements_nutrient("나이아신", ".")
add_supplements_nutrient("비타민B6", ".")
add_supplements_nutrient("엽산", ".")
add_supplements_nutrient("비타민B12", ".")
add_supplements_nutrient("판토텐산", ".")
add_supplements_nutrient("비오틴", ".")
add_supplements_nutrient("칼슘", ".")
add_supplements_nutrient("인", ".")
add_supplements_nutrient("나트륨", ".")
add_supplements_nutrient("염소", ".")
add_supplements_nutrient("칼륨", ".")
add_supplements_nutrient("마그네슘", ".")
add_supplements_nutrient("철", ".")
add_supplements_nutrient("아연", ".")
add_supplements_nutrient("구리", ".")
add_supplements_nutrient("불소", ".")
add_supplements_nutrient("망간", ".")
add_supplements_nutrient("요오드", ".")
add_supplements_nutrient("셀레늄", ".")
add_supplements_nutrient("몰데브덴", ".")
add_supplements_nutrient("스테로이드", ".")
add_supplements_nutrient("프레드니솔론", ".")
add_supplements_nutrient("베타카로틴", ".")
add_supplements_nutrient("제니칼", ".")
add_supplements_nutrient("콜레스티라민", ".")
add_supplements_nutrient("페노바르비탈", ".")
add_supplements_nutrient("페니토인", ".")
add_supplements_nutrient("푸로세미드", ".")
add_supplements_nutrient("플루오로우라실", ".")
add_supplements_nutrient("발프론산", ".")
add_supplements_nutrient("카바마제핀", ".")
add_supplements_nutrient("사이클로세린", ".")
add_supplements_nutrient("클로람페니콜", ".")
add_supplements_nutrient("메트포르민", ".")
add_supplements_nutrient("클로렐라", ".")
add_supplements_nutrient("스피루리나", ".")
add_supplements_nutrient("비타민B1", ".")

"""
# 데이터 수정-detail
def update_nutrient_details(name, new_details):
    sql = "UPDATE supplements_nutrient SET details = ? WHERE name = ?"
    cursor.execute(sql, (new_details, name))
    conn.commit()

# 데이터 수정 예시
update_nutrient_details("열량", ".")
update_nutrient_details("단백질", ".")
update_nutrient_details("식이섬유", ".")
update_nutrient_details("수분", ".")
update_nutrient_details("비타민A", "과복용 시: 뇌척수압 상승, 어지러움, 구토, 피부자극, 관절통증흡연자의 경우 다량복용시 폐암 유발. \n영양소 궁합(Bad): 베타카로틴 영양제랑 같이 복용하지 않는 것이 좋음. \n스테로이드, 프레드니솔론과 함께 복용 시 칼슘흡수 방해, 비타민D 활성화 억제, 골밀도 감소가 우려됨. \n제니칼(비만 치료제), 콜레스티라민은 비타민A 등 지용성 비타민의 흡수가 저해될 수 있음. \n페노바르비탈, 페니토인(간질약)은 비타민의 분해를 촉진하고 흡수를 감소시킴.")
update_nutrient_details("비타민D", "과복용 시: 식욕부진, 당뇨, 부정맥, 혈관 조직 석회화가 우려. \n영양소 궁합(Good): 칼슘과 함께 복용하면 칼슘의 흡수율을 높이는 데 도움을 준다.")
update_nutrient_details("비타민E", "과복용 시: 폐암 사망 확률이 높아진다. \n영양소 궁합(Good): 비타민E는 오메가3 지방산과 같이 섭취하게 되면 오메가3 지방산의 흡수율을 높인다. \n영양소 궁합(Bad): 비타민K와 비타민E는 서로 상충되는 작용을 한다.")
update_nutrient_details("비타민K", "영양소 궁합(Bad): 항응고제를 복용 시 비타민K를 복용하는 것에 주의를 요한다. \n비타민K와 비타민E는 서로 상충되는 작용을 한다.")
update_nutrient_details("비타민C", "과복용 시: 설사, 소화불량, 신장결석 증가 위험이 있으며 다량복용 시 삼투효과가 발생함. 또한, 비타민C는 산성이기 때문에 위장질환이 있는 분들은 복용을 추천하지 않음. \n영양소 궁합(Bad): 철과 비타민C는 서로 상충되는 작용을 한다. \n비스포스 포네이트 제제, 철분제, 진통소염제를 복용 시 비타민C 섭취는 피하는 게 좋다.")
update_nutrient_details("티아민", "과복용 시: 티아민은 과복용 시 소변으로 배출되어서 과복용 걱정은 하지 않아도 된다. \n영양소 궁합(Bad): 푸로세미드(이뇨제)는 티아민과 함께 복용 시 비타민B1배설을 촉진한다. \n플루오로우라실은 티아민과 함께 복용 시 티아민 분해 및 활성형을 막는다.")
update_nutrient_details("리보플라빈", "과량 독성과 영양소 상호작용이 없다.")
update_nutrient_details("나이아신", "영양소 궁합(Bad): 나이아신 섭취 시, 고지혈증 약물과 상호작용에 있어서 근육병증이 증가한다.")
update_nutrient_details("비타민B6", "과복용 시: 신체움직임 조절이 떨어지고 통증에 민감하게 되며 광과민 반응이 일어날 수 있다. \n영양소 궁합: 발프론산, 카바마제핀, 페니토인(간질약)은 비타민B6과 함께 섭취 시, 대사와 분해를 촉진한다. \n사이클로세린(결핵 치료 항생제)는 비타민 B6의 배설을 촉진한다.")
update_nutrient_details("엽산", ".")
update_nutrient_details("비타민B12", "과복용 시:IOM. 과량복용해도 상관 없다. \n영양소 궁합(Bad): 클로람페니콜(항생제)와 메트포르민(당뇨약)은 비타민B12의 흡수를 방해한다.")
update_nutrient_details("판토텐산", ".")
update_nutrient_details("비오틴", ".")
update_nutrient_details("칼슘", "과복용 시: 협십증 등 심혈관 질환, 우울증, 변비, 결석을 유발할 수 있다. \n영양소 궁합(Good): 마그네슘과 같이 복용하면 시너지효과가 일어난다. \n영양소 궁합(Bad): 클로렐라(단백질 보충용), 스피루리나(녹색플랑크톤 식물), 아미노산 제재 등의 단백질은 칼슘의 흡수를 방해한다.")
update_nutrient_details("인", ".")
update_nutrient_details("나트륨", ".")
update_nutrient_details("염소", ".")
update_nutrient_details("칼륨", ".")
update_nutrient_details("마그네슘", "과복용 시: 심신이 심하게 이완되어 맥박이 느려지는 부작용이 일어난다.")
update_nutrient_details("철", "영양소 궁합(Bad): 비타민C, 아연과 서로 상충되는 작용을 한다.")
update_nutrient_details("아연", "영양소 궁합(Bad): 구리는 아연의 흡수를 방해하며 철은 아연과 서로 상충되는 작용을 한다.")
update_nutrient_details("구리", "과복용 시 : 몸에 축적 시 간 독성과 신경 독성. \n영양소 궁합(Bad): 아연과 철분제는 역효과로 구리의 흡수를 방해한다. \n클로렐라(단백질 보충용), 스피루리나(녹색플랑크톤 식물), 아미노산 제재 등의 단백질은 칼슘의 흡수를 방해한다.")
update_nutrient_details("불소", ".")
update_nutrient_details("망간", ".")
update_nutrient_details("요오드", ".")
update_nutrient_details("셀레늄", ".")
update_nutrient_details("몰리브덴", ".")
"""

# 데이터 수정
def update_nutrient_name(old_name, new_name):
    sql = "UPDATE supplements_nutrient SET name = ? WHERE name = ?"
    cursor.execute(sql, (new_name, old_name))
    conn.commit()

# 데이터 수정 예시
update_nutrient_name("에너지", "열량")
update_nutrient_name("비타민 B6", "비타민B6")
# 연결 닫기 (중요)
conn.close()
