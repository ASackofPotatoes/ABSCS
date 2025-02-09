from django.shortcuts import render
from django.http import HttpResponse
from .models import Mnemonic

MAX_MNEMONICS = 12


def addTestMnemonics():
    if Mnemonic.objects.filter(id='1'):
        return
    mnemonic = Mnemonic(type='int', value='36.2', unit='C', name='BATT_TEMP')
    mnemonic.save()


def index(request):
    addTestMnemonics()
    mnemonics = list(Mnemonic.objects.all().values())

    leftToRender = 0

    if (len(mnemonics) >= MAX_MNEMONICS):
        leftToRender = 0
    else:
        leftToRender = MAX_MNEMONICS - len(mnemonics)

    context = {
        "mnemonics": mnemonics[:MAX_MNEMONICS],
        "leftToRender": range(leftToRender)
    }

    print(mnemonics)
    return render(request, "page.html", context)
# Create your views here.
