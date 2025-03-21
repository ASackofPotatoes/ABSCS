from django.urls import path
from . import views

urlpatterns = [
    path("api/set-mission", views.setMission, name="setMission"),
]