from django.shortcuts import HttpResponseRedirect, render

from home import models


def bilan(request, date):
    bilan = list(models.get_bilan(date))
    print(bilan[0])
    return render(request, 'bilan.html', {
        'bilans': bilan
    })
