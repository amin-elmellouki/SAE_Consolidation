import csv

from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.contrib import messages

from .models import Matiere, Etudiant, EstNote, Conso, Bilan, QCM, Participe, RepondreBilan, DemandeEn, MatiereForm
from .models import get_weeks, load_bilan_into_db, load_qcm_into_db, get_qcm_by_week, get_prev_url


@login_required(login_url='/login/')
def home(request):
    semaines = {}
    bilans = get_weeks()

    for bilan in bilans:
        date = str(bilan.dateB)
        qcm_count = get_qcm_by_week(date)
        conso_exists = Conso.objects.filter(dateC=bilan.dateB).exists()

        semaines[date] = {
            'count_qcm': qcm_count,
            'conso_exists': conso_exists
        }

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
        'matieres': Matiere.objects.all(),
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


def add_matiere(request):
    if request.method == 'POST':
        form = MatiereForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matière ajoutée avec succès!')

            return redirect('settings')
        else:
            messages.error(request, "Impossible d'ajouter cette matière, elle existe peut-être déjà !")
    else:
        form = MatiereForm()

    return render(request, 'settings.html', {'form': form})


def delete_matiere(request):
    if request.method == 'POST':
        matiere_nom = request.POST.get('matiere')
        try:
            matiere = Matiere.objects.get(nomMat=matiere_nom)
            matiere.delete()
            messages.success(request, f"La matière '{matiere_nom}' a été supprimée avec succès.")
        except Matiere.DoesNotExist:
            messages.error(request, f"La matière '{matiere_nom}' n'existe pas.")
        except Exception as e:
            messages.error(request, f"Erreur lors de la suppression de la matière: {str(e)}")
    
    return redirect('settings')
