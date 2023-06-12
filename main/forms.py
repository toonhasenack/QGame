# forms.py
from django import forms


class PlayerForm(forms.Form):
    name = forms.CharField(max_length=100, label='First Name')
