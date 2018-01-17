from django import forms
from django.forms import ModelForm, Textarea
from DAO.models import Api

class ApiCreateForm(forms.Form):
    path = forms.CharField(max_length=128)
    method = forms.CharField(max_length=8)
    name = forms.CharField(max_length=128)
    note = forms.CharField(max_length=512, required=False)
    status = forms.IntegerField()
    responseJson = forms.CharField(widget=forms.Textarea)

class ApiUpdateForm(forms.Form):
    path = forms.CharField(max_length=128)
    method = forms.CharField(max_length=8)
    name = forms.CharField(max_length=128)
    note = forms.CharField(max_length=512, required=False)
    status = forms.IntegerField()
    responseJson = forms.CharField(widget=forms.Textarea())

