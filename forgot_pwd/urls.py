from django.urls import path
from . import views

urlpatterns = [
    path('forgot_password', views.forgot_password, name='forgot_password'),
]
