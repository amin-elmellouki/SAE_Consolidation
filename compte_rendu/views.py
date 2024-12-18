from django.shortcuts import redirect, render


def compte_rendu(request):
    if request.method != "POST":
        redirect("/")
    
    render(request, 'compte-rendu.html', {})
