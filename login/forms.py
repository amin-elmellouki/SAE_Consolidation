from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class UsernamePasswordLoginForm(AuthenticationForm):
    INVALID_CREDENTIALS_MESSAGE = _("La combinaison nom d'utilisateur et mot de passe est invalide.")
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': _("Entrez votre nom d'utilisateur"),
            'class': 'form-input username-input'
        }),
        label=''
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': _("Entrez votre mot de passe"),
            'class': 'form-input password-input'
        }),
        label=''
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError(
                self.INVALID_CREDENTIALS_MESSAGE,
                code='invalid_login'
            )

        self.cleaned_data['user'] = user
        return self.cleaned_data

    def get_user(self):
        """
        Retourne l'utilisateur authentifié.
        """
        return self.cleaned_data.get('user')
