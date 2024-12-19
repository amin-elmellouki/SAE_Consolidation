from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import bilan

urlpatterns = [
    path('bilan/<str:date>', bilan, name='bilan'),
]
