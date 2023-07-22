from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class User(AbstractUser):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=[('M', '남성'), ('F', '여성')])
    pregnant = models.BooleanField()
    breastfeeding = models.BooleanField()

    recommended = models.ForeignKey('supplements.RecommendedNutrient', on_delete=models.SET_NULL, null=True, related_name='users',)
