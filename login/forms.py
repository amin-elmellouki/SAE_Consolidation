from django import forms
from django.core.exceptions import ValidationError
from .validators import password_strength

class PasswordOnlyForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Entrez votre mot de passe',
                                          'style': 'width: 300px;'}),
        validators=[password_strength],
    )
