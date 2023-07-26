import sqlite3

# 데이터베이스에 연결
conn = sqlite3.connect('db.sqlite3')  # 파일명은 실제 파일의 경로를 써야 합니다.

# 커서 생성
cursor = conn.cursor()
"""
# 데이터 추가
def add_supplements_nutrient(name, details):
    sql = "INSERT INTO supplements_nutrient (name, details) VALUES (?, ?)"
    cursor.execute(sql, (name, details))
    conn.commit()

# 데이터 추가 예시
add_supplements_nutrient("에너지", ".")
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
add_supplements_nutrient("비타민 B6", ".")
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
# 원하는 만큼 데이터를 추가할 수 있습니다.
"""
# 데이터 수정
def update_nutrient_details(name, new_details):
    sql = "UPDATE supplements_nutrient SET details = ? WHERE name = ?"
    cursor.execute(sql, (new_details, name))
    conn.commit()

# 데이터 수정 예시
update_nutrient_details("비타민C", "새로운 비타민 C의 상세 설명입니다.")

# 연결 닫기 (중요)
conn.close()
