from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from page.models import Mnemonic, Page, PageMnemonic, Command
from django.core.exceptions import BadRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MnemonicSerializer, CommandSerializer
import json

def edit_commands(request):
    commands = Command.objects.all().values()
    
    context = {
        'commands': commands
    }

    return render(request, 'commandEdit.html', context)

@api_view(['POST'])
def add_command(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        serializer = CommandSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        raise BadRequest('Invalid request.')
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)