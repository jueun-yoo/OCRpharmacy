# 영양제 상호작용을 처리

#1. 모델 정의(영양제 상호작용 표현 모델) -supplements -> models.py에 정의되어 있음 
#2. 데이터 저장 및 상호작용 체크 및 결과 출력 


# 영양제 상호작용을 위한 모델 정의  -> datacode : add_interaction코드로 이어짐
from django.db import models
from supplements.models import Supplement

import sqlite3
conn = sqlite3.connect('db.sqlites3')
cursor = conn.cursor()

#Supplement 객체를 가져옴
supplement1 = Supplement.objects.get(name='비타민A')
supplement2 = Supplement.objects.get(name='스테로이드')
supplement3 = Supplement.objects.get(name='프레드니솔론')
supplement4 = Supplement.objects.get(name='베타카로틴')
supplement5 = Supplement.objects.get(name='제니칼')
supplement6 = Supplement.objects.get(name='콜레스티라민')
supplement7 = Supplement.objects.get(name='페노바르비탈')
supplement8 = Supplement.objects.get(name='페니토인')
supplement9 = Supplement.objects.get(name='비타민K')
supplement10 = Supplement.objects.get(name='비타민E')
supplement11 = Supplement.objects.get(name='비타민C')
supplement12 = Supplement.objects.get(name='철')
supplement14 = Supplement.objects.get(name='비타민B1')
supplement15 = Supplement.objects.get(name='푸로세미드')
supplement16 = Supplement.objects.get(name='플루오로우라실')
supplement17 = Supplement.objects.get(name='비타민B6')
supplement18 = Supplement.objects.get(name='발프론산')
supplement19 = Supplement.objects.get(name='카바마제핀')
supplement20 = Supplement.objects.get(name='사이클로세린')
supplement21 = Supplement.objects.get(name='비타민B12')
supplement22 = Supplement.objects.get(name='클로람페니콜')
supplement23 = Supplement.objects.get(name='메트포르민')
supplement24 = Supplement.objects.get(name='아연')
supplement25 = Supplement.objects.get(name='구리')
supplement26 = Supplement.objects.get(name='클로렐라')
supplement27 = Supplement.objects.get(name='스피루리나')

def add_intraction(description, supplement1_id, supplement2_id):
    sql = "INSERT INTO supplements_interaction (description, supplement1_id, supplement2_id VALUES (?, ?, ?))"
    cursor.execute(sql, (description, supplement1_id, supplement2_id))
    conn.commit()

# 비타민A와 스테로이드의 상호작용
interaction1 = Interaction.objects.create(description='[비타민A - 스테로이드] 같이 섭취 시 부작용: 비타민 A의 흡수와 대사에 영향을 줄 수 있음')
interaction1.supplements.add(supplement1, supplement2)

# 비타민A와 프레드니솔론의 상호작용
interaction2 = Interaction.objects.create(description='[비타민A - 프레드니솔론] 같이 섭취 시 부작용: 칼슘흡수 방해, 비타민D 활성화 억제, 골밀도 감소 우려 영향을 줄 수 있음')
interaction2.supplements.add(supplement1, supplement3)

# 비타민A와 베타카로틴의 상호작용
interaction3 = Interaction.objects.create(description='[비타민A - 베타카로틴] 같이 섭취 시 부작용: 지용성 비타민 흡수 억제 영향을 줄 수 있음')
interaction3.supplements.add(supplement1, supplement4)

# 비타민A와 제니칼의 상호작용
interaction4 = Interaction.objects.create(description='[비타민A - 제니칼] 같이 섭취 시 부작용: 비타민A 흡수 감소 영향을 줄 수 있음')
interaction4.supplements.add(supplement1, supplement5)

# 비타민A와 콜레스티라민의 상호작용
interaction5 = Interaction.objects.create(description='[비타민A - 콜레스티라민] 같이 섭취 시 부작용: 비타민D를 포함한 지용성 비타민 흡수 억제 영향을 줄 수 있음')
interaction5.supplements.add(supplement1, supplement6)

# 비타민A와 페노바르비탈의 상호작용
interaction6 = Interaction.objects.create(description='[비타민A - 페노바르비탈] 같이 섭취 시 부작용: 비타민 분해 촉진 영향을 줄 수 있음')
interaction6.supplements.add(supplement1, supplement7)

# 비타민A와 페니토인의 상호작용
interaction7 = Interaction.objects.create(description='[비타민A - 페니토인] 같이 섭취 시 부작용: 비타민 분해 촉진 영향을 줄 수 있음')
interaction7.supplements.add(supplement1, supplement8)

#비타민K와 비타민E의 상호작용
interaction8 = Interaction.objects.create(description='[비타민K - 비타민E] 같이 섭취 시 부작용: 서로 상충되어 영향을 미칠 수 있으므로 주의해야 함')
interaction8.supplements.add(supplement9, supplement10)

#비타민C와 철의 상호작용
interaction9 = Interaction.objects.create(description='[비타민C - 철] 같이 섭취 시 부작용: 서로 상충되어 영향을 미칠 수 있으므로 주의해야 함')
interaction9.supplements.add(supplement11, supplement12)

#비타민B1과 푸로세미드의 상호작용
interaction11 = Interaction.objects.create(description='[비타민B1 - 푸로세미드] 같이 섭취 시 부작용: 비타민B1 배설 촉진 영향을 줄 수 있음')
interaction11.supplements.add(supplement14, supplement15)

#비타민B1과 플루오로우라실의 상호작용
interaction12 = Interaction.objects.create(description='[비타민B1 - 플루오로우라실] 같이 섭취 시 부작용: 분해 및 활성형 방지 영향을 줄 수 있으므로 주의해야 함')
interaction12.supplements.add(supplement14, supplement16)

#비타민B6과 발프론산의 상호작용
interaction13 = Interaction.objects.create(description='[비타민B6 - 발프론산] 같이 섭취 시 부작용: 대사, 분해를 촉진하는 영향을 줄 수 있음')
interaction13.supplements.add(supplement17, supplement18)

#비타민B6과 카바마제핀의 상호작용
interaction14 = Interaction.objects.create(description='[비타민B6 - 카바마제핀] 같이 섭취 시 부작용: 대사, 분해를 촉진하는 영향을 줄 수 있음')
interaction14.supplements.add(supplement17, supplement19)

#비타민B6과 사이클로세린의 상호작용
interaction15 = Interaction.objects.create(description='[비타민B6 - 사이클로세린] 같이 섭취 시 부작용: 비타민B6의 배설을 촉진하는 영향을 줄 수 있음')
interaction15.supplements.add(supplement17, supplement20)

#비타민B12과 클로람페니콜의 상호작용
interaction16 = Interaction.objects.create(description='[비타민B12 - 클로람페니콜] 같이 섭취 시 부작용: 비타민B12의 흡수를 방해하는 영향을 줄 수 있음')
interaction16.supplements.add(supplement21, supplement22)

#비타민B12과 메트포르민의 상호작용
interaction17 = Interaction.objects.create(description='[비타민B12 - 메트포르민] 같이 섭취 시 부작용: 비타민B12의 흡수를 방해하는 영향을 줄 수 있음 ')
interaction17.supplements.add(supplement21, supplement23)

#비타민C과 철의 상호작용
interaction18 = Interaction.objects.create(description='[비타민C - 철] 같이 섭취 시 부작용: 서로 상충되어 영향을 미칠 수 있으므로 주의해야 함')
interaction18.supplements.add(supplement11, supplement12)

#아연과 철의 상호작용
interaction19 = Interaction.objects.create(description='[철 - 아연] 같이 섭취 시 부작용: 서로 상충되어 영향을 미칠 수 있으므로 주의해야 함')
interaction19.supplements.add(supplement12, supplement24)

#아연과 구리의 상호작용
interaction20 = Interaction.objects.create(description='[아연 - 구리] 같이 섭취 시 부작용: 아연의 흡수 방해를 초래할 수 있음')
interaction20.supplements.add(supplement24, supplement25)

#클로렐라과 구리의 상호작용
interaction21 = Interaction.objects.create(description='[구리 - 클로렐라] 같이 섭취 시 부작용: 아미노산을 제재하여 단백질이 칼슘의 흡수를 방해함')
interaction21.supplements.add(supplement26, supplement25)

#스피루리나과 구리의 상호작용
interaction22 = Interaction.objects.create(description= '[구리 - 스피루리나] 같이 섭취 시 부작용: 아미노산을 제재하여 단백질이 칼슘의 흡수를 방해함')
interaction22.supplements.add(supplement27, supplement25)


