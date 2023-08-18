from django import forms

class edit_infoForm(forms.Form):
    name = forms.CharField(label='영양소 이름')
    dosage = forms.FloatField(label='함량')
    unit = forms.FloatField(label='단위')
