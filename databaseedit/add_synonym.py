import sqlite3

# 데이터베이스에 연결
conn = sqlite3.connect('db.sqlite3')  # 파일명은 실제 파일의 경로를 써야 합니다.

# 커서 생성
cursor = conn.cursor()

# 데이터 추가
def add_supplements_synonym(name, nutrient_id):
    sql = "INSERT INTO supplements_synonym (name, nutrient_id) VALUES (?, ?)"
    cursor.execute(sql, (name, nutrient_id))
    conn.commit()


# 데이터 추가 예시
add_supplements_synonym("비타민B1", "티아민")
add_supplements_synonym("비타민B2", "리보플라민")

# 원하는 만큼 데이터를 추가할 수 있습니다.

"""
# 데이터 수정
def update_synonym(nutrient_id, name):
    sql = "UPDATE supplements_synonym SET name = ? WHERE nutrient_id = ?"
    cursor.execute(sql, (nutrient_id, name))
    conn.commit()

# 데이터 수정 예시
update_synonym(1, "??")
"""


# 연결 닫기 (중요)
conn.close()
