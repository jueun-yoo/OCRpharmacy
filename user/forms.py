# user/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):
    GENDER_CHOICES = [('M', '남성'), ('F', '여성')]

    username = forms.CharField(label='아이디', max_length=150)
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    name = forms.CharField(label='이름', max_length=100)
    age = forms.IntegerField(label='나이')
    gender = forms.ChoiceField(label='성별', choices=GENDER_CHOICES)

    pregnant = forms.BooleanField(label='임신 여부', required=False)
    breastfeeding = forms.BooleanField(label='수유 여부', required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'age', 'gender', 'pregnant', 'breastfeeding')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['pregnant'].widget.attrs['class'] = 'hidden'
        self.fields['breastfeeding'].widget.attrs['class'] = 'hidden'
        self.fields['pregnant'].required = False
        self.fields['breastfeeding'].required = False

    def clean(self):
        cleaned_data = super().clean()
        gender = cleaned_data.get('gender')

        if gender == 'F':
            self.fields['pregnant'].widget.attrs['class'] = ''
            self.fields['breastfeeding'].widget.attrs['class'] = ''
            self.fields['pregnant'].required = True
            self.fields['breastfeeding'].required = True
        else:
            self.fields['pregnant'].widget.attrs['class'] = 'hidden'
            self.fields['breastfeeding'].widget.attrs['class'] = 'hidden'
            self.fields['pregnant'].required = False
            self.fields['breastfeeding'].required = False