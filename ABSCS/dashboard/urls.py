from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="dashboard"),
    path("api/start-connection", views.startConnection, name="start-connection")
]
