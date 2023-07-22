from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=[('M', '남성'), ('F', '여성')])
    pregnant = models.BooleanField()
    breastfeeding = models.BooleanField()

    recommended = models.ForeignKey('supplements.RecommendedNutrient', on_delete=models.SET_NULL, null=True, related_name='users')

class UserSupplement(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_supplements')
    supplement = models.ForeignKey('supplements.Supplement', on_delete=models.CASCADE, related_name='user_supplements')

    def __str__(self):
        return f'{self.user.username} - {self.supplement.name}'
    
class UserTotalIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nutrient = models.ForeignKey('supplements.RecommendedNutrient', on_delete=models.CASCADE)
    total_intake = models.FloatField(default=0.0)  # 누적 섭취량

    def __str__(self):
        return f'{self.user.username} - {self.total_intake}'
