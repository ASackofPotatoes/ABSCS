from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from page.models import Mnemonic, Page, PageMnemonic
from django.core.exceptions import BadRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MnemonicSerializer
import json
# Create your views here.

MAX_MNEMONICS = 12

#@api_view(['PUT', 'DELETE'])
def edit_pages_api(request, id):

    if request.method == "DELETE":
        try:
            Page.objects.filter(id=id).delete()
            return redirect('edit_pages')
        except:
            return BadRequest

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

#@api_view(['GET'])
def edit_page(request, id):

    if request.method == "GET":
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

def edit_mnemonics(request):
    mnemonics = Mnemonic.objects.all().values()

    if len(mnemonics) > 1:
        mnemonics = mnemonics[1:]
    else:
        mnemonics = []
    
    context = {
        'mnemonics': mnemonics
    }

    return render(request, 'mnemonicsEdit.html', context)

@api_view(['POST', 'DELETE', 'PUT'])
def edit_mnemonic(request, id):
    
    print("HERE")

    if request.method == "DELETE":
        mnemonic = get_object_or_404(Mnemonic, id=id)
        mnemonic.delete()
        return JsonResponse({'message': 'Mnemonic deleted successfully'}, status=200)
    
    
    if request.method == "PUT":
            
            data = json.loads(request.body)
            print(data)
            mnemonic = Mnemonic.objects.get(id=id)
            serializer = MnemonicSerializer(mnemonic, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        raise BadRequest('Invalid request.')
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@api_view(['POST'])
def add_mnemonic(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        serializer = MnemonicSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        raise BadRequest('Invalid request.')
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@api_view(['GET'])
def get_all_mnemonics(request):
    mnemonics = Mnemonic.objects.all()
    serializer = MnemonicSerializer(mnemonics, many=True)
    return Response(serializer.data)
