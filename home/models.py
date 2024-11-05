from django.db import models

class Etudiant(models.Model):
    numE = models.AutoField(primary_key=True)
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

class Qcm(models.Model):
    dateQ = models.DateField()
    matiere = models.CharField(max_length=50)

    class Meta:
        unique_together = ('dateQ', 'matiere')

class Conso(models.Model):
    dateC = models.DateField()
    matiere = models.CharField(max_length=50)

    class Meta:
        unique_together = ('dateC', 'matiere')

class Bilan(models.Model):
    annee = models.IntegerField()
    numSem = models.IntegerField()

    class Meta:
        unique_together = ('annee', 'numSem')

class EstNote(models.Model):
    numE = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    dateQ = models.ForeignKey(Qcm, on_delete=models.CASCADE)
    note = models.DecimalField(max_digits=4, decimal_places=2)

class Participe(models.Model):
    numE = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    dateC = models.ForeignKey(Conso, on_delete=models.CASCADE)

class RepondreBilan(models.Model):
    numE = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    bilan = models.ForeignKey(Bilan, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    demande = models.CharField(max_length=3, choices=[('oui', 'Oui'), ('non', 'Non')])
