# forms.py
from django import forms

class PasswordOnlyForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Entrez votre mot de passe'}),
    )
