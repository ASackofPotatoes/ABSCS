from django.contrib import admin
from page.models import Page, Mnemonic, PageMnemonic
# Register your models here.
admin.site.register(Page)
admin.site.register(Mnemonic)
admin.site.register(PageMnemonic)
