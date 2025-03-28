from django.shortcuts import render
import json
from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def setMission(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse raw JSON body
        mission_name = data.get('mission_name')
        if not mission_name:
            return JsonResponse({'error': 'Missing mission_name parameter.'}, status=400)
        cache.set("current_mission", mission_name)
        return JsonResponse({}, status=200)
    return JsonResponse({'error': 'Request must be POST'}, status=405)

