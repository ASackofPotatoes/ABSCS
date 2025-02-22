from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from .models import Mnemonic, Page, PageMnemonic

MAX_MNEMONICS = 12


def view_page(request, id):
    page = list(Page.objects.filter(id=id).values())[0]
    print(page)
    mnemonics = 12*[None]

    mnemonicsToAdd = PageMnemonic.objects.filter(page_id=page['id'])

    for item in mnemonicsToAdd:
        if item == None or item.mnemonic_id == -1:
            continue
        currentMnemonic = Mnemonic.objects.get(id=item.mnemonic_id)
        mnemonics[item.position-1] = currentMnemonic

    context = {
        "mnemonics": mnemonics,
        "page": page
    }

    return render(request, "page.html", context)


def add_page(request):
    if request.method == 'POST':
        new_page = Page(title=str(request.POST.get("title")))
        Page.save(new_page)

    return view_page(request, new_page.id)
