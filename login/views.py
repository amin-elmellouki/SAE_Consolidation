from django.contrib.auth.views import LoginView
from .forms import UsernamePasswordLoginForm

class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = UsernamePasswordLoginForm
