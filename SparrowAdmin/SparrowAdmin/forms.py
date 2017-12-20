from django import forms

class ApiCreateForm(forms.Form):
    path = forms.CharField(max_length=128)
    method = forms.CharField(max_length=8)
    name = forms.CharField(max_length=128)
    note = forms.CharField(max_length=512)
    status = forms.IntegerField()