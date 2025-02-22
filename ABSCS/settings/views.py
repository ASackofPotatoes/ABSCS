from django.shortcuts import render, redirect
from django.urls import reverse
from page.models import Mnemonic, Page, PageMnemonic
# Create your views here.

MAX_MNEMONICS = 12


def edit_pages_api(request, id):
    if request.method == "POST":
        print(request.POST)

        if request.POST["pageTitle"] != "":
            Page.objects.filter(id=id).update(title=request.POST["pageTitle"])

        for key in request.POST:
            position = key.split('_')[-1]
            if key.startswith('mnemonic_'):
                if request.POST.get(key) == 'null':
                    if PageMnemonic.objects.filter(page_id=id, position=position).exists():
                        PageMnemonic.objects.filter(
                            page_id=id, position=position).update(mnemonic_id=0)

                mnemonic_id = request.POST.get(key)
                if PageMnemonic.objects.filter(page_id=id, position=position).exists():
                    PageMnemonic.objects.filter(
                        page_id=id, position=position).update(mnemonic_id=mnemonic_id)
                else:
                    newPageMnemonic = PageMnemonic.objects.create(
                        position=position, mnemonic_id=mnemonic_id, page_id=id)
                    newPageMnemonic.save()

        return redirect('edit_pages')
    return redirect('edit_pages')


def edit_pages(request):
    # Get a list of all the pages
    pages = Page.objects.all()
    pagesToConfig = []
    for page in pages:
        pagesToConfig.append({
            "title": page.title,
            "url": reverse("edit_page", kwargs={"id": page.id})
        })

    return render(request, "configPages.html", {"pagesToConfig": pagesToConfig})


def edit_page(request, id):
    page = Page.objects.get(id=id)
    mnemonicsToAdd = PageMnemonic.objects.filter(page_id=page.id)

    mnemonicsSelected = 12*[None]

    for item in mnemonicsToAdd:
        if item == None or item.mnemonic_id == None:
            continue
        currentMnemonic = Mnemonic.objects.get(id=item.mnemonic_id)
        mnemonicsSelected[item.position-1] = currentMnemonic

    mnemonicsToRender = list(Mnemonic.objects.all().values())
    context = {
        'preselectedMnemonics': mnemonicsSelected,
        "page": page,
        "mnemonicsToRender": mnemonicsToRender,
        "leftToRender": range(MAX_MNEMONICS),
    }
    return render(request, "pageEdit.html", context)
