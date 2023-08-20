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


add_supplements_synonym("레티놀", "비타민A") # 비타민A 동의어 추가
add_supplements_synonym("레티놀산", "비타민A") # 비타민A 동의어 추가

add_supplements_synonym("콜레칼시페롤", "비타민D") # 비타민D 동의어 추가
add_supplements_synonym("에르고칼시페롤", "비타민D") # 비타민D 동의어 추가
add_supplements_synonym("비타민D2", "비타민D") # 비타민D 동의어 추가
add_supplements_synonym("비타민D3", "비타민D") # 비타민D 동의어 추가
add_supplements_synonym("카세콜칼시페롤", "비타민D") # 비타민D 동의어 추가

    
add_supplements_synonym("토코페롤", "비타민E") # 비타민E 동의어 추가
add_supplements_synonym("토코트리에놀", "비타민E") # 비타민E 동의어 추가
add_supplements_synonym("알파-토코페롤", "비타민E") # 비타민E 동의어 추가
add_supplements_synonym("감마-토코페롤", "비타민E") # 비타민E 동의어 추가
add_supplements_synonym("델타-토코페롤", "비타민E") # 비타민E 동의어 추가

add_supplements_synonym("피로퀴논", "비타민K") # 비타민K 동의어 추가
add_supplements_synonym("메나퀴논", "비타민K") # 비타민K 동의어 추가
add_supplements_synonym("비타민K1", "비타민K") # 비타민K 동의어 추가
add_supplements_synonym("비타민K2", "비타민K") # 비타민K 동의어 추가
add_supplements_synonym("메나테트레논", "비타민K") # 비타민K 동의어 추가
add_supplements_synonym("나프토퀴논", "비타민K") # 비타민K 동의어 추가

add_supplements_synonym("아스코르빈산", "비타민C") # 비타민C 동의어 추가
add_supplements_synonym("L-아스코르빈산", "비타민C") # 비타민C 동의어 추가  
add_supplements_synonym("아스코르베이트", "비타민C") # 비타민C 동의어 추가
add_supplements_synonym("E셀레늄0", "비타민C") # 비타민C 동의어 추가

add_supplements_synonym("니아신아마이드", "나이아신") # 나이아신 동의어 추가
add_supplements_synonym("니코틴아마이드", "나이아신") # 나이아신 동의어 추가
add_supplements_synonym("비타민B3", "나이아신") # 나이아신 동의어 추가
add_supplements_synonym("니아신산", "나이아신") # 나이아신 동의어 추가
add_supplements_synonym("니코틴산", "나이아신") # 나이아신 동의어 추가

add_supplements_synonym("피리독신", "비타민B6") # 비타민B6 동의어 추가
add_supplements_synonym("피리도산", "비타민B6") # 비타민B6 동의어 추가
add_supplements_synonym("피리독암인", "비타민B6") # 비타민B6 동의어 추가
add_supplements_synonym("니코틴산아마이드", "비타민B6") # 비타민B6 동의어 추가
add_supplements_synonym("비타민B6복합체", "비타민B6") # 비타민B6 동의어 추가

add_supplements_synonym("폴릭 애씨드", "엽산") # 엽산 동의어 추가
add_supplements_synonym("비타민B9", "엽산") # 엽산 동의어 추가
add_supplements_synonym("테로일모노글루타민산", "엽산") # 엽산 동의어 추가
add_supplements_synonym("테로일-L-글루타민산", "엽산") # 엽산 동의어 추가


add_supplements_synonym("코발라민", "비타민B12") # 비타민B12 동의어 추가
add_supplements_synonym("시아노코발라민", "비타민B12") # 비타민B12 동의어 추가
add_supplements_synonym("메틸코발라민", "비타민B12") # 비타민B12 동의어 추가
add_supplements_synonym("하이드록시코발라민", "비타민B12") # 비타민B12 동의어 추가

add_supplements_synonym("비타민B1", "판토텐산") # 판토텐산 동의어 추가
add_supplements_synonym("칼슘판토텐산염", "판토텐산") # 판토텐산 동의어 추가
add_supplements_synonym("덱스판텐올", "판토텐산") # 판토텐산 동의어 추가
add_supplements_synonym("D-판토텐산염", "판토텐산") # 판토텐산 동의어 추가

add_supplements_synonym("비타민B7", "비오틴") # 비오틴 동의어 추가
add_supplements_synonym("비타민H", "비오틴") # 비오틴 동의어 추가
add_supplements_synonym("Coenzyme", "비오틴") # 비오틴 동의어 추가

add_supplements_synonym("셀레노시스테인", "셀레늄") # 셀레늄 동의어 추가
add_supplements_synonym("셀레노시스테인", "셀레늄") # 셀레늄 동의어 추가


add_supplements_synonym("몰리브데넘", "몰데브덴") # 몰리브덴 동의어 추가






# 원하는 만큼 데이터를 추가할 수 있습니다.

"""
# 데이터 수정
def update_synonym(old_id, new_id):
    sql = "UPDATE supplements_synonym SET nutrient_id = ? WHERE nutrient_id = ?"
    cursor.execute(sql, (new_id, old_id))
    conn.commit()

# 데이터 수정 예시
update_synonym(5, "비타민A")
update_synonym(6, "비타민D")
update_synonym(7, "비타민E")
update_synonym(8, "비타민K")
update_synonym(9, "비타민C")
update_synonym(12, "나이아신")
update_synonym(13, "비타민B6")
update_synonym(14, "엽산")
update_synonym(15, "비타민B12")
update_synonym(16, "판토텐산산")
update_synonym(17, "비오틴")
update_synonym(30, "셀레늄")
update_synonym(31, "몰데브덴")
"""
# 연결 닫기 (중요)
conn.close()
