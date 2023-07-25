import sqlite3

# 데이터베이스에 연결
conn = sqlite3.connect('db.sqlite3')  # 파일명은 실제 파일의 경로를 써야 합니다.

# 커서 생성
cursor = conn.cursor()

def delete_supplements_recommendednutrient(start_id, end_id):
    sql = "DELETE FROM supplements_recommendednutrient WHERE id BETWEEN ? AND ?"
    cursor.execute(sql, (start_id, end_id))
    conn.commit()

delete_supplements_recommendednutrient() # 계층 id 넣기

# 연결 닫기 (중요)
conn.close()