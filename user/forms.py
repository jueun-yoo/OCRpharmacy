from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(UserCreationForm):
    GENDER_CHOICES = [('남', '남성'), ('여', '여성')]

    username = forms.CharField(label='아이디', max_length=150)
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)
    email = forms.EmailField(label='이메일')

    #name = forms.CharField(label='이름', max_length=100)
    age = forms.IntegerField(label='나이')
    gender = forms.ChoiceField(label='성별', choices=GENDER_CHOICES)

    pregnant = forms.BooleanField(label='임신 여부', required=False)
    breastfeeding = forms.BooleanField(label='수유 여부', required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'age', 'gender', 'pregnant', 'breastfeeding')

class LoginForm(forms.Form):
    username = forms.CharField(label='아이디', max_length=150)
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)