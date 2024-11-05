from django.db import models

class Etudiant(models.Model):
    numE = models.AutoField(primary_key=True)
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

class Matiere(models.Model):
    idMat = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)

class Qcm(models.Model):
    dateQ = models.DateField(primary_key=True)

class Conso(models.Model):
    dateC = models.DateField(primary_key=True)

class CorrespondQcm(models.Model):
    qcm = models.ForeignKey(Qcm, on_delete=models.CASCADE, related_name="correspondances")
    matiere = models.OneToOneField(Matiere, on_delete=models.CASCADE, related_name="qcm_unique")

class CorrespondConso(models.Model):
    conso = models.ForeignKey(Conso, on_delete=models.CASCADE, related_name="correspondances")
    matiere = models.OneToOneField(Matiere, on_delete=models.CASCADE, related_name="conso_unique")

class Bilan(models.Model):
    annee = models.IntegerField()
    numSem = models.IntegerField()

    class Meta:
        unique_together = ('annee', 'numSem')

class EstNote(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    qcm = models.ForeignKey(Qcm, on_delete=models.CASCADE)
    note = models.DecimalField(max_digits=4, decimal_places=2)

class Participe(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    conso = models.ForeignKey(Conso, on_delete=models.CASCADE)

class RepondreBilan(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    bilan = models.ForeignKey(Bilan, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    demande = models.CharField(max_length=3, choices=[('oui', 'Oui'), ('non', 'Non')])
