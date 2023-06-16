# forms.py
from django import forms


class PlayerForm(forms.Form):
    name1 = forms.CharField(max_length=100, label='Player 1 Name')
    name2 = forms.CharField(max_length=100, label='Player 2 Name')
