from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import bilan, export_bilan

urlpatterns = [
    path('bilan/<str:date>', bilan, name='bilan'),
    path('export_bilans/<str:date>', export_bilan, name='export_bilans'),
]
