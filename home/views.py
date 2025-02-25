import csv

from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render

from .models import Matiere, get_weeks, load_bilan_into_db, load_qcm_into_db, get_qcm_by_week


@login_required(login_url='/login/')
def home(request):
    semaines = {}
    bilans = get_weeks()

    for bilan in bilans:
        date = str(bilan.dateB)
        qcm_count = get_qcm_by_week(date)
        semaines[date] = qcm_count

    context = {
        'message': "Bienvenue, vous êtes connecté !",
        'user': request.user,
        'matieres': Matiere.objects.all(),
        'semaines': semaines, 
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
