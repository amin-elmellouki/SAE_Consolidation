from django.contrib import admin
from django.urls import path

from .views import compte_rendu, conso, delete_student, set_absent

urlpatterns = [
    path('conso/<str:date>/submit/', compte_rendu, name='compte_rendu'),
    path('conso/<str:date>/', conso, name='conso'),
    path('delete_stu/<str:etudiant_id>/<int:conso_id>/', delete_student, name='delete_stu'),
    path('set_absent/', set_absent, name='set_absent'),
]
