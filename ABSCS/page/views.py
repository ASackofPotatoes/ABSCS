from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from .models import Mnemonic, Page, PageHasMnemonic

MAX_MNEMONICS = 12


def getAllPages():
    pages = Page.objects.all()
    pageList = []
    for page in pages:
        pageList.append({
            "title": page.title,
            "url": reverse("view", kwargs={"id": page.id})
        })
    return pageList


def view_page(request, id):
    page = list(Page.objects.filter(id=id).values())[0]
    mnemonicIds = list(PageHasMnemonic.objects.filter(
        pageId=id).values_list('mnemonicId'))
    mnemonics = []
    try:
        for item in mnemonicIds:
            mnemonics.append(
                list(Mnemonic.objects.filter(id=item[0]).values())[0])
    except:
        pass

    leftToRender = 0

    if (len(mnemonics) >= MAX_MNEMONICS):
        leftToRender = 0
    else:
        leftToRender = MAX_MNEMONICS - len(mnemonics)

    context = {
        "page": page,
        "mnemonics": mnemonics[:MAX_MNEMONICS],
        "leftToRender": range(leftToRender),
        "listPages": getAllPages()
    }

    return render(request, "page.html", context)


def edit(request):
    mnemonics = list(Mnemonic.objects.all().values())
    context = {
        "mnemonicsToRender": mnemonics,
        "leftToRender": range(MAX_MNEMONICS)
    }
    return render(request, "pageEdit.html", context)


def add_page(request):
    if request.method == 'POST':
        new_page = Page(title=str(request.POST.get("title")))
        Page.save(new_page)

    return view_page(request, new_page.id)
