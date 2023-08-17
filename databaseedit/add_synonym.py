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

# add_supplements_synonym("비타민B1", "10") # 티아민 동의어 추가
# add_supplements_synonym("비타민B2", "11") # 리보플라민 동의어 추가


add_supplements_synonym("레티놀", "5") # 비타민A 동의어 추가
add_supplements_synonym("레티놀산", "5") # 비타민A 동의어 추가

add_supplements_synonym("콜레칼시페롤", "6") # 비타민D 동의어 추가
add_supplements_synonym("에르고칼시페롤", "6") # 비타민D 동의어 추가
add_supplements_synonym("비타민D2", "6") # 비타민D 동의어 추가
add_supplements_synonym("비타민D3", "6") # 비타민D 동의어 추가
add_supplements_synonym("카세콜칼시페롤", "6") # 비타민D 동의어 추가

    
add_supplements_synonym("토코페롤", "7") # 비타민E 동의어 추가
add_supplements_synonym("토코트리에놀", "7") # 비타민E 동의어 추가
add_supplements_synonym("알파-토코페롤", "7") # 비타민E 동의어 추가
add_supplements_synonym("감마-토코페롤", "7") # 비타민E 동의어 추가
add_supplements_synonym("델타-토코페롤", "7") # 비타민E 동의어 추가

add_supplements_synonym("피로퀴논", "8") # 비타민K 동의어 추가
add_supplements_synonym("메나퀴논", "8") # 비타민K 동의어 추가
add_supplements_synonym("비타민K1", "8") # 비타민K 동의어 추가
add_supplements_synonym("비타민K2", "8") # 비타민K 동의어 추가
add_supplements_synonym("메나테트레논", "8") # 비타민K 동의어 추가
add_supplements_synonym("나프토퀴논", "8") # 비타민K 동의어 추가

add_supplements_synonym("아스코르빈산", "9") # 비타민C 동의어 추가
add_supplements_synonym("L-아스코르빈산", "9") # 비타민C 동의어 추가  
add_supplements_synonym("아스코르베이트", "9") # 비타민C 동의어 추가
add_supplements_synonym("E300", "9") # 비타민C 동의어 추가

add_supplements_synonym("니아신아마이드", "12") # 나이아신 동의어 추가
add_supplements_synonym("니코틴아마이드", "12") # 나이아신 동의어 추가
add_supplements_synonym("비타민B3", "12") # 나이아신 동의어 추가
add_supplements_synonym("니아신산", "12") # 나이아신 동의어 추가
add_supplements_synonym("니코틴산", "12") # 나이아신 동의어 추가

add_supplements_synonym("피리독신", "13") # 비타민B6 동의어 추가
add_supplements_synonym("피리도산", "13") # 비타민B6 동의어 추가
add_supplements_synonym("피리독암인", "13") # 비타민B6 동의어 추가
add_supplements_synonym("니코틴산아마이드", "13") # 비타민B6 동의어 추가
add_supplements_synonym("비타민B6복합체", "13") # 비타민B6 동의어 추가

add_supplements_synonym("폴릭 애씨드", "14") # 엽산 동의어 추가
add_supplements_synonym("비타민B9", "14") # 엽산 동의어 추가
add_supplements_synonym("테로일모노글루타민산", "14") # 엽산 동의어 추가
add_supplements_synonym("테로일-L-글루타민산", "14") # 엽산 동의어 추가


add_supplements_synonym("코발라민", "15") # 비타민B12 동의어 추가
add_supplements_synonym("시아노코발라민", "15") # 비타민B12 동의어 추가
add_supplements_synonym("메틸코발라민", "15") # 비타민B12 동의어 추가
add_supplements_synonym("하이드록시코발라민", "15") # 비타민B12 동의어 추가

add_supplements_synonym("비타민B5", "16") # 판토텐산 동의어 추가
add_supplements_synonym("칼슘판토텐산염", "16") # 판토텐산 동의어 추가
add_supplements_synonym("덱스판텐올", "16") # 판토텐산 동의어 추가
add_supplements_synonym("D-판토텐산염", "16") # 판토텐산 동의어 추가

add_supplements_synonym("비타민B7", "17") # 비오틴 동의어 추가
add_supplements_synonym("비타민H", "17") # 비오틴 동의어 추가
add_supplements_synonym("Coenzyme", "17") # 비오틴 동의어 추가

add_supplements_synonym("셀레노시스테인", "30") # 셀레늄 동의어 추가
add_supplements_synonym("셀레노시스테인", "30") # 셀레늄 동의어 추가


add_supplements_synonym("몰리브데넘", "31") # 몰리브덴 동의어 추가






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
