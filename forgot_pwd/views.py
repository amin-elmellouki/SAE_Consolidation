from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Validation du format de l'email
        try:
            validate_email(email)
        except ValidationError:
            return HttpResponse("L'email fourni n'est pas valide.", status=400)

        # Vérification si l'utilisateur existe
        if User.objects.filter(email=email).exists():
            try:
                send_mail(
                    'Réinitialisation de mot de passe',
                    'Cliquez sur ce lien pour réinitialiser votre mot de passe.',
                    'noreply@example.com',  # Email expéditeur
                    [email],  # Email destinataire
                    fail_silently=False,
                )
            except Exception as e:
                return HttpResponse(f"Une erreur s'est produite : {e}", status=500)

        # Message générique pour éviter de révéler si l'email existe
        return HttpResponse("Si cet email est enregistré, un lien de réinitialisation a été envoyé.")

    # Affiche le formulaire de réinitialisation
    return render(request, 'forgot_password.html')
