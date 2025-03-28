from django.db import models

class Mission(models.Model):
    #Top-level mission table
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    model_type = "config"