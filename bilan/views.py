from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, render

from home import models


def export_bilan(request, date):
    bilan = list(models.get_bilan(date))
    wb = models.generate_excel(bilan)
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.ms-excel'
    )
    response['Content-Disposition'] = f'attachment; filename="bilans-du-{date}.xls"'
    
    return response


def bilan(request, date):
    bilan = list(models.get_bilan(date))
    
    return render(request, 'bilan.html', {
        'bilans': bilan,
        'date': date,
        'matieres': models.Matiere.objects.all(),
    })
