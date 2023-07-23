from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    nickname = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=[('M', '남성'), ('F', '여성')])
    age = models.PositiveIntegerField()

    class Meta:
        app_label = 'accounts'  # 해당 모델이 속한 앱의 이름

    def __str__(self):
        return self.username

