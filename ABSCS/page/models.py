from django.db import models


class Mnemonic(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=200)
    name = models.CharField(max_length=200, default="noName")
    value = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class PageMnemonic(models.Model):
    page = models.ForeignKey(
        'Page', on_delete=models.CASCADE, related_name='mnemonics')
    mnemonic = models.ForeignKey(
        'Mnemonic', on_delete=models.SET_NULL, null=True)
    position = models.PositiveIntegerField()

    class Meta:
        unique_together = ('page', 'position')

    def __str__(self):
        return f"{self.page.title} - Mnemonic {self.position}"


class Page(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
