from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class User(AbstractUser):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender_choices = [
        ('F', '여성'),
        ('M', '남성'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices, null=True, blank=True)
    is_pregnant = models.BooleanField(default=False)
    is_breastfeeding = models.BooleanField(default=False)
