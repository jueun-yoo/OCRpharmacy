import sqlite3

# 데이터베이스에 연결
conn = sqlite3.connect('db.sqlite3')  # 파일명은 실제 파일의 경로를 써야 합니다.

# 커서 생성
cursor = conn.cursor()
"""
# 데이터 추가
def add_supplements_recommendedintake(gender, age_start, age_end, pregnant, breastfeeding):
    sql = "INSERT INTO supplements_recommendedintake (gender, age_start, age_end, pregnant, breastfeeding) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(sql, (gender, age_start, age_end, pregnant, breastfeeding))
    conn.commit()

# 데이터 추가 예시
add_supplements_recommendedintake("남", 6, 8, False, False)
add_supplements_recommendedintake("남", 9, 11, False, False)
add_supplements_recommendedintake("남", 12, 14, False, False)
add_supplements_recommendedintake("남", 15, 18, False, False)
add_supplements_recommendedintake("남", 19, 29, False, False)
add_supplements_recommendedintake("남", 30, 49, False, False)
add_supplements_recommendedintake("남", 50, 64, False, False)
add_supplements_recommendedintake("남", 65, 74, False, False)
add_supplements_recommendedintake("남", 75, 200, False, False)
add_supplements_recommendedintake("여", 6, 8, False, False)
add_supplements_recommendedintake("여", 9, 11, False, False)
add_supplements_recommendedintake("여", 12, 14, False, False)
add_supplements_recommendedintake("여", 15, 18, False, False)
add_supplements_recommendedintake("여", 19, 29, False, False)
add_supplements_recommendedintake("여", 30, 49, False, False)
add_supplements_recommendedintake("여", 50, 64, False, False)
add_supplements_recommendedintake("여", 65, 74, False, False)
add_supplements_recommendedintake("여", 75, 200, False, False)
add_supplements_recommendedintake("여", 12, 14, True, False)
add_supplements_recommendedintake("여", 15, 18, True, False)
add_supplements_recommendedintake("여", 19, 29, True, False)
add_supplements_recommendedintake("여", 30, 49, True, False)
add_supplements_recommendedintake("여", 50, 64, True, False)
add_supplements_recommendedintake("여", 12, 14, False, True)
add_supplements_recommendedintake("여", 15, 18, False, True)
add_supplements_recommendedintake("여", 19, 29, False, True)
add_supplements_recommendedintake("여", 30, 49, False, True)
add_supplements_recommendedintake("여", 50, 64, False, True)
# 원하는 만큼 데이터를 추가할 수 있습니다.
"""
# 연결 닫기 (중요)
conn.close()