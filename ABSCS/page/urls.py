from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_page, name="add"),
    path("<int:id>/", views.view_page, name="view"),
]
