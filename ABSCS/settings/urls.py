from django.urls import include, path
from . import views

urlpatterns = [
    path("api/editpage/<int:id>", views.edit_pages_api, name="edit_page_api"),
    path("api/mnemonics", views.get_all_mnemonics, name="get_all_mnemonics"),
    path("page/", views.edit_pages, name="edit_pages"),
    path("page/<int:id>", views.edit_page, name="edit_page"),
    path("mnemonics", views.edit_mnemonics, name="edit_mnemonics"),
    path("api/editmnemonic/<int:id>", views.edit_mnemonic, name="edit_mnemonic"),
    path("api/addmnemonic", views.add_mnemonic, name="add_mnemonic"),
]
