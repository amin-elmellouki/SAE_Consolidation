from django.shortcuts import HttpResponseRedirect, render

from home import models


def bilan(request, date):
    bilan = list(models.get_bilan(date))
    return render(request, 'bilan.html', {
        'bilans': bilan,
        'date': date,
    })
