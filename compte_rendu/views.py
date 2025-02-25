import json

from django.shortcuts import redirect, render

from home.models import consolider_etudiant, get_etudiant


def compte_rendu(request):
    if request.method != "POST":
        return redirect("/")
    
    body = request.body.decode('utf-8') 
    data = json.loads(body)
    
    # Enregistre dans le bd
    for matiere, etudiants in data["conso"].items():
        for etudiant in etudiants:
            consolider_etudiant(data["date"], matiere, etudiant)
    
    for matiere, etudiants in data["conso"].items():
        data["conso"][matiere] = [get_etudiant(numero) for numero in etudiants]
    return render(request, 'compte-rendu.html', {'data': data["conso"]})
