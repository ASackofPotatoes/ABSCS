from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import Mnemonic
from tcp_client.tcp_handler import tcp_client
import threading
import asyncio

from django.urls import reverse
from django.http import HttpResponse
from page.models import Page
MAX_MNEMONICS = 12


def getAllPages():
    pages = Page.objects.all()
    print(pages)
    pageList = []
    for page in pages:
        pageList.append({
            "title": page.title,
            "url": reverse("view", kwargs={"id": page.id})
        })
    return pageList


@csrf_exempt
def startConnection(request):
    # GET DATABASE CONNECTION PROFILE FROM REQUEST BODY
    ip = "127.0.0.1"
    port = 12345

    # Start a new thread to run the asyncio event loop
    thread = threading.Thread(target=asyncio.run, args=(tcp_client(ip, port),))
    thread.start()

    return JsonResponse({"message": "Connection attempted"})


def index(request):
    return render(request, "index.html", {"listPages": getAllPages()})
# Create your views here.
