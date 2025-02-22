from django.urls import include, path
from . import views

urlpatterns = [
    path("api/editpage/<int:id>", views.edit_pages_api, name="edit_page_api"),
    path("page/", views.edit_pages, name="edit_pages"),
    path("page/<int:id>", views.edit_page, name="edit_page"),
]
