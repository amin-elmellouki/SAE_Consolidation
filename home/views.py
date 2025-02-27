import csv

from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render, redirect

from .models import Matiere, Etudiant, EstNote, Conso, Bilan, QCM, Participe, RepondreBilan, DemandeEn
from .models import get_weeks, load_bilan_into_db, load_qcm_into_db, get_qcm_by_week, get_prev_url


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
    file = request.FILES.getlist('file')[0]
    load_bilan_into_db(file)
    
    return HttpResponseRedirect("/")


@login_required(login_url="/login/")
def load_qcm(request):
    file = request.FILES.getlist('file')[0]
    load_qcm_into_db(file, request.POST.get('matiere'))
    
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def settings(request):
    context = {
        'previous_url': get_prev_url(request),
    }
    return render(request, 'settings.html', context)


@login_required(login_url='/login/')
def delete_bd(request):
    try:
        Participe.objects.all().delete()
        EstNote.objects.all().delete()
        RepondreBilan.objects.all().delete()
        DemandeEn.objects.all().delete()
        QCM.objects.all().delete()
        Bilan.objects.all().delete()
        Conso.objects.all().delete()
        Matiere.objects.all().delete()
        Etudiant.objects.all().delete()

    except Exception as e:
        print(e)

    return redirect('settings')