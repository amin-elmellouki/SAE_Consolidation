from django.db import models


class Matiere(models.Model):
    nomMat = models.CharField(max_length=100, primary_key=True)


class QCM(models.Model):
    dateQ = models.DateField(primary_key=True)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name="qcms")


class Etudiant(models.Model):
    numE = models.AutoField(primary_key=True)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


class Conso(models.Model):
    dateC = models.DateField(primary_key=True)
    etudiants = models.ManyToManyField(Etudiant, through="Participe")


class Bilan(models.Model):
    annee = models.IntegerField()
    numSem = models.IntegerField()
    etudiants = models.ManyToManyField(Etudiant, through="RepondreBilan")

    class Meta:
        unique_together = (('annee', 'numSem'),)


class Participe(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    conso = models.ForeignKey(Conso, on_delete=models.CASCADE)


class EstNote(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    qcm = models.ForeignKey(QCM, on_delete=models.CASCADE)
    note = models.DecimalField(max_digits=5, decimal_places=2)


class RepondreBilan(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    bilan = models.ForeignKey(Bilan, on_delete=models.CASCADE)
    desc = models.TextField()
    demande = models.TextField()
