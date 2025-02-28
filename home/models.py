import csv
from urllib.parse import urlparse

import xlwt
from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import get_object_or_404
from xlwt import Workbook, easyxf


class Matiere(models.Model):
    nomMat = models.CharField(max_length=100, primary_key=True)

    class Meta:
        indexes = [
            models.Index(fields=['nomMat']),
        ]

class QCM(models.Model):
    dateQ = models.DateField()
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name="qcms")

    class Meta:
        indexes = [
            models.Index(fields=['dateQ']),
        ]
        unique_together = ('dateQ', 'matiere')


class Etudiant(models.Model):
    numE = models.CharField(primary_key=True, max_length=100)
    nomPrenom = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    groupe = models.CharField(max_length=3)
    
    class Meta:
        indexes = [
            models.Index(fields=['numE']),
        ]


class Conso(models.Model):
    dateC = models.DateField()
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name="consos")
    etudiants = models.ManyToManyField(Etudiant, through="Participe")
    
    class Meta:
        unique_together = ("dateC", "matiere")
        
        indexes = [
            models.Index(fields=['dateC']),
        ]


class Bilan(models.Model):
    dateB = models.DateField(primary_key=True)
    etudiants = models.ManyToManyField(Etudiant, through="RepondreBilan")
    
    class Meta:
        indexes = [
            models.Index(fields=['dateB']),
        ]


class Participe(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    conso = models.ForeignKey(Conso, on_delete=models.CASCADE)
    estAbsent = models.BooleanField(default=False)

    class Meta:
        unique_together = ('etudiant', 'conso')
        indexes = [
            models.Index(fields=['etudiant', 'conso'])
        ]


class EstNote(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    qcm = models.ForeignKey(QCM, on_delete=models.CASCADE)
    note = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['etudiant'])
        ]
        unique_together = ('etudiant', 'qcm')


class RepondreBilan(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    bilan = models.ForeignKey(Bilan, on_delete=models.CASCADE)
    desc = models.TextField()
    demande = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['etudiant', 'bilan'])
        ]
        unique_together = ('etudiant', 'bilan')


class DemandeEn(models.Model):
    reponse = models.ForeignKey(RepondreBilan, on_delete=models.CASCADE, related_name='matieres')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='demandes')
    
    indexes = [
        models.Index(fields=['matiere', 'reponse'])
    ]


class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = ['nomMat']
        labels = {
            'nomMat': 'Nom de la matière',
        }


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

def get_weeks():
    return Bilan.objects.all()
    

def format_bilan_date(date: str) -> str:
    date = date.replace(',', '').split(' ')
    return f"{date[3]}-{MONTHS[date[2]]}-{date[1]}"


def format_qcm_date(date: str) -> str:
    date = date.split(" ")
    return f"{date[2]}-{MONTHS[date[1]]}-{date[0]}"


def load_bilan_into_db(file):
    reader = csv.DictReader(file.read().decode('utf-8').splitlines(), delimiter="\t")
    
    for row in reader:
        date_bilan = format_bilan_date(row['Date'])
        bilan, _ = Bilan.objects.get_or_create(dateB=date_bilan)
        
        etudiant, _ = Etudiant.objects.get_or_create(
            numE=row['Numéro d’identification'],
            defaults={
                'nomPrenom': row['Nom complet de l’utilisateur'],
                'email': row['Adresse de courriel'],
                'groupe': row['Groupes'],
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
                if len(matiere_name.strip()) > 0: 
                    matiere, _ = Matiere.objects.get_or_create(nomMat=matiere_name.strip())
                    DemandeEn.objects.get_or_create(reponse=reponse, matiere=matiere)


def load_qcm_into_db(file, nom_matiere):
    reader = csv.DictReader(file.read().decode('utf-8').splitlines(), delimiter="\t")
    
    matiere = Matiere.objects.get(nomMat=nom_matiere)
    for row in reader:
        if row['Nom de famille'] == 'Moyenne globale':
            continue
        
        date_qcm = format_qcm_date(row['Commencé le'])
        qcm, _ = QCM.objects.get_or_create(dateQ=date_qcm, matiere=matiere)
        
        etudiant, _ = Etudiant.objects.get_or_create(
            numE=row['Numéro d’identification'],
            defaults={
                'nomPrenom': f"{row['Nom de famille']} {row['Prénom']}",
                'email': row['Adresse de courriel']
            }
        )
        
        try:
            note = float(row['Note/20,00'].replace(',', '.'))
        except ValueError:
            raise ValidationError("La note n'est pas au format valide")
        
        est_note, _ = EstNote.objects.get_or_create(
            etudiant=etudiant,
            qcm=qcm,
            defaults={'note': note}
        )
        
        if est_note.note != note:
            est_note.note = note
            est_note.save()


def get_notes_by_stu(num_etud):
    notes_by_mat = EstNote.objects.filter(
        etudiant__numE=num_etud).select_related('qcm__matiere', 'etudiant')

    res = {}
    for est_note in notes_by_mat:
        matiere = est_note.qcm.matiere.nomMat
        note = float(est_note.note)
        
        if matiere in res:
            res[matiere].append(note)
        else:
            res[matiere] = [note]

    return res


def get_bilan(date):
    reponses_bilan = RepondreBilan.objects.filter(
        bilan=Bilan.objects.get(dateB=date)
    )
    
    for reponse_bilan in reponses_bilan:
        notes_dict = {}
        notes = EstNote.objects.filter(
            etudiant=Etudiant.objects.get(numE=reponse_bilan.etudiant.numE),
            qcm__dateQ=date
        )

        for note in notes:
            notes_dict[note.qcm.matiere.nomMat] = note.note

        matieres_demandees = ", ".join(
            demande.matiere.nomMat 
            for demande in DemandeEn.objects.filter(reponse=reponse_bilan)
        )

        notes_by_mat = get_notes_by_stu(reponse_bilan.etudiant.numE)

        yield {
            'numE': reponse_bilan.etudiant.numE,
            'nom': reponse_bilan.etudiant.nomPrenom.split(' ')[0],
            'prenom': reponse_bilan.etudiant.nomPrenom.split(' ')[1],
            'groupe': reponse_bilan.etudiant.groupe,
            'desc': reponse_bilan.desc,
            'demande': reponse_bilan.demande,
            'demande_en': matieres_demandees,
            'notes': notes_dict,
            'notes_by_mat': notes_by_mat,
            'historique': get_historique_conso(reponse_bilan.etudiant.numE),
        }


def consolider_etudiant(date: str, matiere: str, numero_etudiant: str):
    conso, _created = Conso.objects.get_or_create(
        dateC=date,
        matiere=Matiere.objects.get(nomMat=matiere)
    )
    
    etudiant = Etudiant.objects.get(numE=numero_etudiant)
    
    if not Participe.objects.filter(etudiant=etudiant, conso=conso).exists():
        Participe.objects.create(
            etudiant=etudiant,
            conso=conso,
            estAbsent=False,
        )


def get_students_from_conso(date):
    result = {}
    consos = Conso.objects.filter(dateC=date).select_related('matiere')
    
    for conso in consos:
        participations = Participe.objects.filter(conso=conso).select_related('etudiant')
        
        if not participations.exists():
            conso.delete()
            continue
        
        students_dict = {
            participation.etudiant: participation.estAbsent
            for participation in participations
        }
        
        result[conso.matiere.nomMat] = {
            'id': conso.id,
            'students': students_dict
        }

    return result


def delete_student_from_conso(etudiant_id, conso_id):
    etudiant = get_object_or_404(Etudiant, numE=etudiant_id)
    conso = get_object_or_404(Conso, id=conso_id)
    
    participation = Participe.objects.filter(etudiant=etudiant, conso=conso)
    
    if participation.exists():
        participation.delete()


def get_qcm_by_week(date):
    return QCM.objects.filter(dateQ=date).count()


def get_etudiant(numero_etudiant: str) -> Etudiant:
    return Etudiant.objects.get(numE=numero_etudiant)


def get_historique_conso(numero_etudiant: str) -> dict:
    matieres = Matiere.objects.all()
    res = {matiere.nomMat: [] for matiere in matieres}
    bilans = RepondreBilan.objects.filter(etudiant__numE=numero_etudiant)
    max_len = bilans.count()
    
    for repondre_bilan in bilans:
        bilan_date = repondre_bilan.bilan.dateB
        demandes = DemandeEn.objects.filter(reponse=repondre_bilan)
        
        for demande in demandes:
            matiere = demande.matiere
            
            participe = Participe.objects.filter(
                etudiant__numE=numero_etudiant,
                conso__dateC=bilan_date,
                conso__matiere=matiere,
            ).first()
        
            # Je m'excuse solennellement pour ce code.
            # Je sais que c'est moche.
            # Je sais que c'est possible de faire mieux.
            # Mais je refuse de toucher à plus de JS
            if participe and participe.estAbsent:
                if demande:
                    res[matiere.nomMat].append("<span class='tag black'>Oui</span>") # A demandé et a été absent
                else:
                    res[matiere.nomMat].append("<span class='tag black'>Non</span>") # N'a pas demandé et a été absent

            else:
                if participe and demande:
                    res[matiere.nomMat].append("<span class='tag green'>Oui</span>") # A demandé et est inscrit
                
                elif participe:
                    res[matiere.nomMat].append("<span class'tag green'>Non</span>") #Est inscrit sans avoir demandé

                elif demande:
                    res[matiere.nomMat].append("<span class='tag red'>Oui</span>") #A demandé sans avoir été inscrit
                
                else:
                    res[matiere.nomMat].append("<span>Non</span>") # N'est pas inscrit, n'a pas demandé
    
    for matiere in matieres:
        current_len = len(res[matiere.nomMat])
        if current_len < max_len:
            res[matiere.nomMat].extend(["<span>Non</span>"] * (max_len - current_len))
    
    return res


def generate_excel(bilans):
    wb = Workbook(encoding='utf-8')
    ws = wb.add_sheet('Bilans Étudiants')

    header_style = easyxf(
        'font: bold on; '
        'align: wrap on, vert centre, horiz center; '
        'pattern: pattern solid, fore_colour light_green;'
    )

    if not bilans:
        return wb 

    matieres = list(bilans[0]['notes'].keys())
    
    headers = [
        'Numéro étudiant',
        'Nom', 
        'Prénom',
        'Groupe'
    ]
    
    headers += [f'QCM {matiere} (/20)' for matiere in matieres]
    
    headers += [
        'Demande conso.',
        'Commentaires',
    ]
    
    for col, header in enumerate(headers):
        ws.write(0, col, header, header_style)
    
        if header == 'Commentaires':
            ws.col(col).width = 8000  
        else:
            ws.col(col).width = 3000  

    normal_style = easyxf('align: vert centre')

    for row_idx, bilan in enumerate(bilans, 1):
        
        ws.write(row_idx, 0, bilan['numE'], normal_style)
        ws.write(row_idx, 1, bilan['nom'], normal_style)
        ws.write(row_idx, 2, bilan['prenom'], normal_style)
        ws.write(row_idx, 3, bilan['groupe'], normal_style)
        
        
        for col_offset, matiere in enumerate(matieres, 4):
            ws.write(row_idx, col_offset, bilan['notes'][matiere], normal_style)
        
        demande_col = 4 + len(matieres)
        ws.write(row_idx, demande_col, bilan['demande_en'], normal_style)
        ws.write(row_idx, demande_col + 1, bilan['desc'], normal_style)

    return wb


def get_conso_by_date(date):
    return Conso.objects.get(dateC=date)


def get_date_conso(conso_id):
    conso = get_object_or_404(Conso, id=conso_id)
    return conso.dateC


def get_prev_url(request):
    previous_url = request.META.get('HTTP_REFERER', '/')
    current_url = request.build_absolute_uri()
    parsed_url = urlparse(previous_url).path if previous_url != current_url else '/'
    return parsed_url
