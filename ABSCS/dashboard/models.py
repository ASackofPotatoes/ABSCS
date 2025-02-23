from django.db import models

class Mission(models.Model):
    #Top-level mission table
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class Connection_Profile(models.Model):
    id = models.AutoField(primary_key=True)
    mission_id = models.IntegerField()
    name = models.CharField(max_length=200)
    protocol = models.CharField(max_length=200) # How to restrict this to a set of possible values (should only be "TCP" right now)
    ip = models.CharField(max_length=16)
    port = models.IntegerField()

