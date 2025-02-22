from page.models import Page
from django.urls import reverse


def header_data(request):
    pages = Page.objects.all()
    pageList = []
    for page in pages:
        pageList.append({
            "title": page.title,
            "url": reverse("view", kwargs={"id": page.id})
        })
    pageList = {"pageList": pageList}
    return pageList
