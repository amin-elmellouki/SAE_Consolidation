import csv

from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render

from .models import Matiere, get_weeks, load_bilan_into_db, load_qcm_into_db


@login_required(login_url='/login/')
def home(request):
    context = {
        'message': "Bienvenue, vous êtes connecté !",
        'user': request.user,
        'matieres': Matiere.objects.all(),
        'semaines': map(lambda x: str(x.dateB), get_weeks()),
    }
    return render(request, 'home.html', context)


@login_required(login_url="/login/")
def load_bilan(request):
    files = request.FILES.getlist('files')
    for file in files:
        load_bilan_into_db(file)
    
    return HttpResponseRedirect("/")


@login_required(login_url="/login/")
def load_qcm(request):
    files = request.FILES.getlist('files')
    for file in files:
        load_qcm_into_db(file, request.POST.get('matiere'))
    
    return HttpResponseRedirect("/")
