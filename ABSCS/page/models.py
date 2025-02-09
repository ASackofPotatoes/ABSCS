from django.db import models


class Page(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)


class Mnemonic(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=200)
    name = models.CharField(max_length=200, default="noName")
    value = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)


class PageHasMnemonic(models.Model):
    id = models.AutoField(primary_key=True)
    pageId = models.IntegerField
    mnemonicId = models.IntegerField
