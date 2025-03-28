from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.core.cache import cache
from tcp_client.tcp_handler import tcp_client
import threading
import asyncio
import json

from django.urls import reverse
from django.http import HttpResponse
from page.models import Page
from .models import Connection_Profile
from missions.models import Mission
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

def getAllMissions():
    missions = Mission.objects.using("default").all()
    missionList = []
    for mission in missions:
        missionList.append({
            "name": mission.name,
        })
    return missionList

    
@csrf_exempt
def startConnection(request):
    if request.method == 'POST':
        try:
            # Parse JSON from request body
            data = json.loads(request.body)
            mission_name = data.get('mission_name')
            profile_name = data.get('profile_name')

            if (cache.get("current_mission") is mission_name) and (cache.get("profile_name") is profile_name):
                return JsonResponse({'error': 'Already connected to this profile!'})
            # Validate inputs
            if not mission_name or not profile_name:
                return JsonResponse({'error': 'mission_name and profile_name are required.'}, status=400)

            profile = Connection_Profile.objects.using(mission_name).get(name=profile_name)

            ip = profile.ip
            port = profile.port

            # Start a new thread to run the asyncio event loop
            thread = threading.Thread(target=asyncio.run, args=(tcp_client(ip, port,
                                                                           mission_name=mission_name,
                                                                           profile_name=profile_name),))
            thread.start()

            return JsonResponse({"message": f"Connection attempted to {ip}:{port}"})

        except Connection_Profile.DoesNotExist:
            return JsonResponse({'error': 'Connection Profile not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


@csrf_exempt
def getConnectionProfiles(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse raw JSON body
        mission_name = data.get('mission_name')
        profiles = Connection_Profile.objects.using(mission_name).all()
        profileList = []
        for profile in profiles:
            profileList.append({"name" : profile.name,
                                "protocol" : profile.protocol,
                                "ip" : profile.ip,
                                "port" : profile.port})
        if not mission_name:
            return JsonResponse({'error': 'Missing mission_name parameter.'}, status=400)
        return JsonResponse({"profiles" : profileList})
    return JsonResponse({'error': 'Request must be POST'}, status=405)


def index(request):
    return render(request, "index.html", {"listPages": [],
                                          "missionList" : getAllMissions()})
# Create your views here.
