from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class UsernamePasswordLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': "Entrez votre nom d'utilisateur",
            'style': 'width: 220px;'
        }),
        label=""
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Entrez votre mot de passe',
            'style': 'width: 220px;'
        }),
        label=""
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError(
                _("La combinaison nom d'utilisateur et mot de passe est invalide."),
                code='invalid_login'
            )
        # Vérification supplémentaire : permet aux superutilisateurs de bypass les règles
        if user.is_superuser:
            self.cleaned_data['user'] = user
            return self.cleaned_data

        self.cleaned_data['user'] = user
        return self.cleaned_data

    def get_user(self):
        return self.cleaned_data.get('user')
