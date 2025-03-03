from django.apps import AppConfig
from django.db.models.signals import post_migrate


def populate_matieres(sender, **kwargs):
    from .models import Matiere
    initial_matieres = ["Maths", "HTML/CSS", "Bash", "Python", "BD", "IJVM", "Java"]
    
    for matiere in initial_matieres:
        Matiere.objects.get_or_create(nomMat=matiere)


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'


    def ready(self):
        post_migrate.connect(populate_matieres, sender=self)