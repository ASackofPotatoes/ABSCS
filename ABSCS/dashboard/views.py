from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import Mnemonic
from tcp_client.tcp_handler import tcp_client
import threading
import asyncio

MAX_MNEMONICS = 12


def addTestMnemonics():
    if Mnemonic.objects.filter(id='1'):
        return
    mnemonic = Mnemonic(type='int', value='36.2', unit='C', name='BATT_TEMP')
    mnemonic.save()

@csrf_exempt
def startConnection(request):
    ###GET DATABASE CONNECTION PROFILE FROM REQUEST BODY
    ip = "127.0.0.1"
    port = 12345

    # Start a new thread to run the asyncio event loop
    thread = threading.Thread(target=asyncio.run, args=(tcp_client(ip, port),))
    thread.start()   

    return JsonResponse({"message":"Connection attempted"})

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
    return render(request, "index.html", context)
# Create your views here.
