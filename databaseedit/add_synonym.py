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

"""
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
"""

add_supplements_synonym("Calories", "열량")
add_supplements_synonym("calories", "열량")
add_supplements_synonym("Protein", "단백질")
add_supplements_synonym("protein", "단백질")
add_supplements_synonym("DietaryFieber", "식이섬유")
add_supplements_synonym("dietaryfiber", "식이섬유")
add_supplements_synonym("Water", "수분")
add_supplements_synonym("water", "수분")
add_supplements_synonym("VitaminA", "비타민A")
add_supplements_synonym("vitaminA", "비타민A")
add_supplements_synonym("VitaminD", "비타민D")
add_supplements_synonym("vitaminD", "비타민D")
add_supplements_synonym("VitaminE", "비타민E")
add_supplements_synonym("vitaminE", "비타민E")
add_supplements_synonym("VitaminK", "비타민K")
add_supplements_synonym("vitaminK", "비타민K")
add_supplements_synonym("VitaminC", "비타민C")
add_supplements_synonym("vitaminC", "비타민C")
add_supplements_synonym("Thiamin", "티아민")
add_supplements_synonym("thiamin", "티아민")
add_supplements_synonym("VitaminB1", "티아민")
add_supplements_synonym("vitaminB1", "티아민")
add_supplements_synonym("Riboflavin", "리보플라민")
add_supplements_synonym("riboflavin", "리보플라민")
add_supplements_synonym("VitaminB2", "리보플라민")
add_supplements_synonym("vitaminb2", "리보플라민")
add_supplements_synonym("Niacin", "나이아신")
add_supplements_synonym("niacin", "나이아신")
add_supplements_synonym("VitaminB3", "나이아신")
add_supplements_synonym("vitaminB3", "나이아신")
add_supplements_synonym("VitaminB6", "비타민B6")
add_supplements_synonym("vitaminB6", "비타민B6")
add_supplements_synonym("Floate", "엽산")
add_supplements_synonym("floate", "엽산")
add_supplements_synonym("VitaminB9", "엽산")
add_supplements_synonym("vitaminB9", "엽산")
add_supplements_synonym("VitaminB12", "비타민B12")
add_supplements_synonym("vitaminB12", "비타민B12")
add_supplements_synonym("PantothenicAcid", "판토텐산")
add_supplements_synonym("pantothenicacid", "판토텐산")
add_supplements_synonym("Biotin", "비오틴")
add_supplements_synonym("biotin", "비오틴")
add_supplements_synonym("Calcium", "칼슘")
add_supplements_synonym("calcium", "칼슘")
add_supplements_synonym("Phosphorus", "인")
add_supplements_synonym("phosphorus", "인")
add_supplements_synonym("Sodium", "나트륨")
add_supplements_synonym("sodium", "나트륨")
add_supplements_synonym("Potassium", "칼륨")
add_supplements_synonym("potassium", "칼륨")
add_supplements_synonym("Magnesium", "마그네슘")
add_supplements_synonym("magnesium", "마그네슘")
add_supplements_synonym("Iron", "철")
add_supplements_synonym("iron", "철")
add_supplements_synonym("Zinc", "아연")
add_supplements_synonym("zinc", "아연")
add_supplements_synonym("Copper", "구리")
add_supplements_synonym("copper", "구리")
add_supplements_synonym("Fluorine", "불소")
add_supplements_synonym("fluorine", "불소")
add_supplements_synonym("Manganese", "망간")
add_supplements_synonym("manganese", "망간")
add_supplements_synonym("Iodine", "요오드")
add_supplements_synonym("iodine", "요오드")
add_supplements_synonym("Selenium", "셀레늄")
add_supplements_synonym("selenium", "셀레늄")
add_supplements_synonym("Molybdenum", "몰데브덴")
add_supplements_synonym("molybdenum", "몰데브덴")
add_supplements_synonym("Prednisolone", "프레드니솔론")
add_supplements_synonym("prednisolone", "프레드니솔론")
add_supplements_synonym("Beta-Carotene", "베타카로틴")
add_supplements_synonym("BetaCarotene", "베타카로틴")
add_supplements_synonym("beta-carotene", "베타카로틴")
add_supplements_synonym("betacarotene", "베타카로틴")
add_supplements_synonym("Xenical", "제니칼")
add_supplements_synonym("xenical", "제니칼")
add_supplements_synonym("Cholestyramine", "콜레스티라민")
add_supplements_synonym("cholestyramine", "콜레스티라민")
add_supplements_synonym("Phenobarbital", "페노바르비탈")
add_supplements_synonym("phenobarbital", "페노바르비탈")
add_supplements_synonym("Phenytoin", "페니토인")
add_supplements_synonym("phenytoin", "페니토인")
add_supplements_synonym("Furosemide", "푸로세미드")
add_supplements_synonym("furosemide", "푸로세미드")
add_supplements_synonym("Fluorouracil", "플루오로우라실")
add_supplements_synonym("fluorouracil", "플루오로우라실")
add_supplements_synonym("ValproicAcid", "발프론산")
add_supplements_synonym("valproicacid", "발프론산")
add_supplements_synonym("Carbamazepine", "카바마제핀")
add_supplements_synonym("carbamazepine", "카바마제핀")
add_supplements_synonym("Cycloserine", "사이클로세린")
add_supplements_synonym("cycloserine", "사이클로세린")
add_supplements_synonym("Chloramphenicol", "클로람페니콜")
add_supplements_synonym("chloramphenicol", "클로람페니콜")
add_supplements_synonym("Metformin", "메트포르민")
add_supplements_synonym("metformin", "메트포르민")



# 연결 닫기 (중요)
conn.close()
