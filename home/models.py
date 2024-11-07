import csv

from django.core.exceptions import ValidationError
from django.db import models


class Matiere(models.Model):
    nomMat = models.CharField(max_length=100, primary_key=True)


class QCM(models.Model):
    dateQ = models.DateField(primary_key=True)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name="qcms")


class Etudiant(models.Model):
    numE = models.CharField(primary_key=True, max_length=100)
    nomPrenom = models.CharField(max_length=200)
    email = models.EmailField(unique=True)


class Conso(models.Model):
    dateC = models.DateField(primary_key=True)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name="consos")
    etudiants = models.ManyToManyField(Etudiant, through="Participe")


class Bilan(models.Model):
    dateB = models.DateField(primary_key=True)
    etudiants = models.ManyToManyField(Etudiant, through="RepondreBilan")


class Participe(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    conso = models.ForeignKey(Conso, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('etudiant', 'conso')


class EstNote(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    qcm = models.ForeignKey(QCM, on_delete=models.CASCADE)
    note = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        unique_together = ('etudiant', 'qcm')


class RepondreBilan(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    bilan = models.ForeignKey(Bilan, on_delete=models.CASCADE)
    desc = models.TextField()
    demande = models.TextField()
    
    class Meta:
        unique_together = ('etudiant', 'bilan')


class DemandeEn(models.Model):
    reponse = models.ForeignKey(RepondreBilan, on_delete=models.CASCADE, related_name='matieres')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='demandes')


def get_or_add_matiere(nom):
    if Matiere.objects.filter(nomMat=nom).exists():
        return Matiere.objects.get(nomMat=nom)
    
    matiere = Matiere(nomMat=nom)
    matiere.save()
    return matiere


def get_or_add_student(num_e, nom_prenom, email):
    if Etudiant.objects.filter(numE=num_e).exists():
        return Etudiant.objects.get(numE=num_e)
    
    etudiant = Etudiant(
        numE=num_e,
        nomPrenom=nom_prenom,
        email=email
    )
    etudiant.save()
    return etudiant


months = {
    'janvier': 1,
    'fevrier': 2,
    'mars': 3,
    'avril': 4,
    'mai': 5,
    'juin': 6,
    'juillet': 7,
    'août': 8,
    'septembre': 9,
    'octobre': 10,
    'novembre': 11,
    'décembre': 12,
}

def formar_date(date: str) -> str:
    date = date.replace(',', '').split(' ')
    return f"{date[3]}-{months[date[2]]}-{date[1]}"


# Gestion de l'ajout du bilan
def get_or_add_bilan(date):
    if Bilan.objects.filter(dateB=date).exists():
        return Bilan.objects.get(dateB=date)
    
    bilan = Bilan(dateB=date)
    bilan.save()
    return bilan 


def add_reponse_bilan(etudiant: Etudiant, bilan: Bilan, desc: str, demande: bool) -> RepondreBilan:
     reponse = RepondreBilan(
         etudiant=etudiant,
         bilan=bilan,
         desc=desc,
         demande=demande
     )
     reponse.save()
     print('Bilan ajouté')
     return reponse


def load_bilan_into_db(file):
    reader = csv.DictReader(file.read().decode('utf-8').splitlines(), delimiter="	")
    
    for row in reader:
        bilan = get_or_add_bilan(formar_date(row['Date']))
        
        etudiant = get_or_add_student(
            row['Numéro d’identification'],
            row['Nom complet de l’utilisateur'],
            row['Adresse de courriel']
            )
        
        demande_conso = row['Consolidation'] == 'Oui'
        reponse = add_reponse_bilan(
            etudiant,
            bilan,
            row['Précisions'],
            demande_conso 
        )
        
        if demande_conso:
            for matiere in row['Matière'].split("  "):
                DemandeEn(reponse=reponse, matiere=get_or_add_matiere(matiere)).save()


def load_qcm_into_db(file):
    pass
