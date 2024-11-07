import csv

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


def get_or_add_matiere(nom: str) -> Matiere:
    matiere, _ = Matiere.objects.get_or_create(nomMat=nom)
    return matiere


def get_or_add_student(num_e: str, nom_prenom: str, email: str) -> Etudiant:
    etudiant, _ = Etudiant.objects.get_or_create(numE=num_e, defaults={'nomPrenom': nom_prenom, 'email': email})
    return etudiant


MONTHS = {
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


def format_date(date: str) -> str:
    parts = date.replace(',', '').split(' ')
    return f"{parts[3]}-{MONTHS[parts[2]]}-{parts[1]}"


def get_or_add_bilan(date: str) -> Bilan:
    bilan, _ = Bilan.objects.get_or_create(dateB=date)
    return bilan


def add_reponse_bilan(etudiant: Etudiant, bilan: Bilan, desc: str, demande: bool) -> RepondreBilan:
    reponse = RepondreBilan.objects.create(
        etudiant=etudiant,
        bilan=bilan,
        desc=desc,
        demande=demande
    )
    return reponse


def load_bilan_into_db(file) -> None:
    reader = csv.DictReader(file.read().decode('utf-8').splitlines(), delimiter="\t")
    
    for row in reader:
        date_bilan = format_date(row['Date'])
        bilan, _ = Bilan.objects.get_or_create(dateB=date_bilan)
        
        etudiant, _ = Etudiant.objects.get_or_create(
            numE=row['Numéro d’identification'],
            defaults={
                'nomPrenom': row['Nom complet de l’utilisateur'],
                'email': row['Adresse de courriel']
            }
        )
        
        demande_conso = row['Consolidation'] == 'Oui'
        
        reponse, _ = RepondreBilan.objects.get_or_create(
            etudiant=etudiant,
            bilan=bilan,
            defaults={
                'desc': row['Précisions'],
                'demande': demande_conso
            }
        )
        
        if demande_conso:
            for matiere_name in row['Matière'].split("  "):
                matiere, _ = Matiere.objects.get_or_create(nomMat=matiere_name)
                DemandeEn.objects.get_or_create(reponse=reponse, matiere=matiere)


def load_qcm_into_db(file) -> None:
    pass
