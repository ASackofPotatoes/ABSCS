from django.shortcuts import render
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


def index(request):
    return render(request, "index.html", {"listPages": getAllPages()})
# Create your views here.
