import json

from django.shortcuts import redirect, render


def compte_rendu(request):
    if request.method != "POST":
        return redirect("/")
    
    body = request.body.decode('utf-8') 
    data = json.loads(body)
    
    print(data)
    return render(request, 'compte-rendu.html', {'data': data})

