from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .validators import password_strength

class UsernamePasswordLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Entrez votre nom d\'utilisateur',
            'style': 'width: 185px;'
        }),
        label=_("")
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Entrez votre mot de passe',
            'style': 'width: 185px;'
        }),
        validators=[password_strength],
        label=_("")
    )
