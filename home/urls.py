from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import home, load_bilan, load_qcm, settings, delete_bd, add_matiere, delete_matiere

urlpatterns = [
    path('', home, name='home'),
    path('load_bilan', load_bilan, name='load_bilan'),
    path('load_qcm', load_qcm, name='load_qcm'),
    path('settings', settings, name='settings'),
    path('delete_bd', delete_bd, name='delete_bd'),
    path('add-matiere/', add_matiere, name='add_matiere'),
    path('delete_mat', delete_matiere, name='delete_matiere')
]
