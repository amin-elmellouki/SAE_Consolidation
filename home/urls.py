from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import home

urlpatterns = [
    path('', home, name='home'),
]
