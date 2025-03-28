from page.models import Page
from django.urls import reverse
from django.core.cache import cache

def header_data(request):
    current_mission = cache.get("current_mission")
    if current_mission:
        pages = Page.objects.using(current_mission).all()
        pageList = []
        for page in pages:
            pageList.append({
                "title": page.title,
                "url": reverse("view", kwargs={"id": page.id})
            })
        pageList = {"pageList": pageList}
        return pageList
    else:
        return []
