import re
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

def password_strength(password):
    validate_password(password)

    #Au moins un caractère spécial
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Le mot de passe doit contenir au moins un caractère spécial (!@#$%^&*(),.?\":{}|<>).")
    
    #Au moins une lettre majuscule
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Le mot de passe doit contenir au moins une lettre majuscule.")
    
    #Au moins une lettre minuscule
    if not re.search(r'[a-z]', password):
        raise ValidationError("Le mot de passe doit contenir au moins une lettre minuscule.")
    
    #Au moins un chiffre
    if not re.search(r'\d', password):
        raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")
    
    #Pas d'espaces
    if re.search(r'\s', password):
        raise ValidationError("Le mot de passe ne doit pas contenir d'espaces.")
    
    # Pas de répétitions consécutives de caractères identiques
    if re.search(r'(.)\1', password):
        raise ValidationError("Le mot de passe ne doit pas contenir de répétitions consécutives de caractères identiques.")
