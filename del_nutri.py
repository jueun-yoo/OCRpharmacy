import sqlite3

# 데이터베이스에 연결
conn = sqlite3.connect('db.sqlite3')  # 파일명은 실제 파일의 경로를 써야 합니다.

# 커서 생성
cursor = conn.cursor()

def delete_supplements_nutrient(name):
    sql = "DELETE FROM supplements_nutrient WHERE name = ?"
    cursor.execute(sql, (name,))
    conn.commit()

delete_supplements_nutrient("") # 영양소 이름 넣기

# 연결 닫기 (중요)
conn.close()