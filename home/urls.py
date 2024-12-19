from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import home, load_bilan, load_qcm

urlpatterns = [
    path('', home, name='home'),
    path('load_bilan', load_bilan, name='load_bilan'),
    path('load_qcm', load_qcm, name='load_qcm'),
]
