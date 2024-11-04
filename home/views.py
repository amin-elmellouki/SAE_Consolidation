from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/login/')
def home(request):
    context = {
        'message': "Bienvenue, vous êtes connecté !",
        'user': request.user
    }
    return render(request, 'home.html', context)
