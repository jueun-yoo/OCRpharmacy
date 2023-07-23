from django.db import models
from django.contrib.auth.models import AbstractUser

#사용자이고, 위의 조건을 입력하면 자동으로 해당하는 권장량 table의 pk가 부여. (signal.py 확인)
class User(AbstractUser):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=[('M', '남성'), ('F', '여성')])
    pregnant = models.BooleanField(default=False)
    breastfeeding = models.BooleanField(default=False)

    recommended = models.OneToOneField('supplements.RecommendedIntake', on_delete=models.SET_NULL, null=True, related_name='users')
    intake = models.ManyToManyField('supplements.Nutrient', through='UserIntake')


class UserIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nutrient = models.ForeignKey('supplements.Nutrient', on_delete=models.CASCADE)
    dosage = models.FloatField(default=0.0)


#누적에 대한 정의는 여기 말고 view에서 하기로 해요..