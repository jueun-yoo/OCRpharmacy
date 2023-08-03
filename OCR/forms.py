from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class OCRResultEditForm(forms.Form):
    edited_ocr_result = forms.CharField(widget=forms.Textarea)