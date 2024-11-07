from django.conf import settings
from django.shortcuts import render, redirect
from .forms import PasswordOnlyForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password

def password_login_view(request):
    if request.method == 'POST':
        form = PasswordOnlyForm(request.POST)
        if form.is_valid():
            entered_password = form.cleaned_data['password']
            if check_password(entered_password, settings.UNIQUE_PASSWORD_HASH):
                request.session['authenticated'] = True
                return redirect('home')
            else:
                messages.error(request, "Mot de passe incorrect.")
    else:
        form = PasswordOnlyForm()

    return render(request, 'login.html', {'form': form})
