from django.db import models

#영양소 1개 정보
class Nutrient(models.Model): 
    name = models.CharField(max_length=200)
    details = models.TextField()

    def __str__(self):
        return self.name

#영양소의 동의어 처리 - 하나의 영양소에 대해 여러개의 동의어 생성
class Synonym(models.Model):
    nutrient = models.ForeignKey(Nutrient, related_name='synonyms', on_delete=models.CASCADE)
    synonym = models.CharField(max_length=200)

    def __str__(self):
        return self.synonym

#영양제 데이터, 영양제 이름과 여러개의 영양소 연결
class Supplement(models.Model):
    name = models.CharField(max_length=200)
    nutrients = models.ManyToManyField(Nutrient, through='SupplementNutrient')

    def __str__(self):
        return self.name

#영양제와 영양소 데이터의 관계. "복용량" 데이터 추가를 위해서!!
class SupplementNutrient(models.Model):
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE)
    dosage = models.FloatField(default=0.0)


class RecommendedNutrient(models.Model):
    gender = models.CharField(max_length=1, choices=[('M', '남성'), ('F', '여성')])
    age_start = models.IntegerField()  # 시작 나이
    age_end = models.IntegerField()    # 끝나는 나이
    pregnant = models.BooleanField()
    breastfeeding = models.BooleanField()

    nutrients = models.ManyToManyField(Nutrient, through='RecommendedIntake')

class RecommendedIntake(models.Model):
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    recommended_intake = models.ForeignKey(RecommendedNutrient, on_delete=models.CASCADE)
    dosage = models.FloatField(default=0.0)
