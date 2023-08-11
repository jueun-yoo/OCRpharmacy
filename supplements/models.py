from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import UserTotalIntake

#영양소 1개 정보
class Nutrient(models.Model): 
    name = models.CharField(max_length=200)
    details = models.TextField()

    def __str__(self):
        return self.name

#영양소의 동의어 처리 - 하나의 영양소에 대해 여러개의 동의어 생성
class Synonym(models.Model):
    nutrient = models.ForeignKey(Nutrient, related_name='synonyms', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

#영양제 데이터, 영양제 이름과 여러개의 영양소, 그리고 입력한 사용자 연결
class Supplement(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='supplement')
    name = models.CharField(max_length=200)
    nutrients = models.ManyToManyField(Nutrient, through='SupplementNutrient')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
  

#영양제와 영양소 데이터의 관계. "복용량" 데이터 추가를 위해서!!
#이거는 중간 모델이고, 영양제와 연결하려면 위의 모델(Supplement) 써야함
class SupplementNutrient(models.Model):
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE)
    dosage = models.FloatField(default=0.0)



#적정섭취량 모델. 조건들 + 영양소와 다대다로 엮어서 하나의 적정섭취량과 여러 영양소 연결
class RecommendedIntake(models.Model):
    gender = models.CharField(max_length=1, choices=[('M', '남성'), ('F', '여성')])
    age_start = models.IntegerField()  # 시작 나이
    age_end = models.IntegerField()    # 끝나는 나이
    pregnant = models.BooleanField()
    breastfeeding = models.BooleanField()

    nutrients = models.ManyToManyField(Nutrient, through='RecommendedNutrient')

#적정섭취 - 영양소 연결 시 추가 필요한 복용량 데이터를 삽입하기 위한 중간 class.
#동일하게 참조 시에는 RecommendedIntake class 참조하세요
class RecommendedNutrient(models.Model):
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    recommended_intake = models.ForeignKey(RecommendedIntake, on_delete=models.CASCADE)
    dosage = models.FloatField(default=0.0)