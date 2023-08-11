from django import forms
from django.contrib.postgres.fields import JSONField  # JSONField 추가
from .models import Supplement

class SupplementForm(forms.ModelForm):
    class Meta:
        model = Supplement
        fields = ['name']  # 필요한 필드 추가

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class OCRResultEditForm(forms.Form):
    edited_ocr_result = forms.JSONField(widget=forms.Textarea)
