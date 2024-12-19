import json

from django.shortcuts import redirect, render

from home.models import get_etudiant


def compte_rendu(request):
    if request.method != "POST":
        return redirect("/")
    
    body = request.body.decode('utf-8') 
    data = json.loads(body)
    
    for matiere, etudiants in data.items():
        data[matiere] = [get_etudiant(numero) for numero in etudiants]
    
    return render(request, 'compte-rendu.html', {'data': data})

