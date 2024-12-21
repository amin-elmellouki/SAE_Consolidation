from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class UsernamePasswordLoginForm(AuthenticationForm):
    """
    Formulaire personnalisé pour l'authentification des utilisateurs.

    Hérite de `AuthenticationForm` pour fournir un formulaire adapté avec des champs 
    de nom d'utilisateur et de mot de passe personnalisés.
    """
    
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
        """
        Valide les informations d'identification fournies.

        Vérifie que la combinaison nom d'utilisateur et mot de passe correspond à un utilisateur valide.
        Si la validation échoue, lève une `ValidationError` avec un message approprié.
        
        Returns:
            dict: Les données nettoyées avec l'utilisateur authentifié inclus.

        Raises:
            forms.ValidationError: Si l'authentification échoue.
        """
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

        Cette méthode est utile pour récupérer l'utilisateur après une validation réussie.

        Returns:
            User: L'utilisateur authentifié ou None.
        """
        return self.cleaned_data.get('user')
