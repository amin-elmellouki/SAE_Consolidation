from django.contrib.auth.views import LoginView
from django.shortcuts import render


class CustomLoginView(LoginView):
    template_name = 'login.html'  # Nom du template pour la page de connexion
