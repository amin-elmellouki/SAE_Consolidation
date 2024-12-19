from django.contrib import admin
from django.urls import path

from .views import compte_rendu

urlpatterns = [
    path('compte_rendu/', compte_rendu),
]
