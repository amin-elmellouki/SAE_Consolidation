import json

from django.shortcuts import redirect, render, get_object_or_404

from home.models import consolider_etudiant, get_students_from_conso, get_prev_url, delete_student_from_conso, get_date_conso
from home.models import Etudiant, Conso, Participe


def compte_rendu(request, date=None):
    if request.method == "POST":
        body = request.body.decode('utf-8')
        data = json.loads(body)

        # Enregistre dans le bd
        for matiere, etudiants in data["conso"].items():
            for etudiant in etudiants:
                consolider_etudiant(data["date"], matiere, etudiant)
        
    return redirect('conso', date=date)
    

def conso(request, date):
    context = {
        'data': get_students_from_conso(date),
        'date': date,
        'previous_url': get_prev_url(request),
    }
    return render(request, 'conso.html', context)


def delete_student(request, etudiant_id, conso_id):
    delete_student_from_conso(etudiant_id, conso_id)
    date = get_date_conso(conso_id)
    return redirect('conso', date=date)


def set_absent(request, date=None):
    if request.method == 'POST':
        data = json.loads(request.body)
        etudiant_id = data.get('etudiant_id')
        conso_id = data.get('conso_id')

        etudiant = Etudiant.objects.get(pk=etudiant_id)
        conso = Conso.objects.get(pk=conso_id)

        participation = Participe.objects.get(etudiant=etudiant, conso=conso)
        participation.estAbsent = not participation.estAbsent
        participation.save()

        date = conso.dateC

    return redirect('conso', date=date)
