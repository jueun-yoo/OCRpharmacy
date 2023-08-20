from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, age, gender, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, age=age, gender=gender, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, age, gender, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(username, email, age, gender, password, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField()

    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=[('남', '남성'), ('여', '여성')])
    pregnant = models.BooleanField(default=False)
    breastfeeding = models.BooleanField(default=False)
    recommended = models.ForeignKey('supplements.RecommendedIntake', on_delete=models.SET_NULL, null=True, related_name='users')
    totalintake = models.ManyToManyField('supplements.Nutrient', through='UserTotalIntake')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'age', 'gender']

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def __str__(self):
        return self.username
    
class UserTotalIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nutrient = models.ForeignKey('supplements.Nutrient', to_field='name', on_delete=models.CASCADE)
    dosage = models.FloatField(default=0.0)
    unit = models.CharField(max_length=10, default='TEMP')


    
#누적에 대한 정의는 여기 말고 view에서 하기로 해요..