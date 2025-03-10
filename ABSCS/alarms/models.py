from django.db import models
from dashboard.models import Mission
from page.models import Mnemonic

class Alarms(models.Model):    
    id = models.AutoField(primary_key=True)
    mission_id = models.ForeignKey(Mission)
    mnemonic_id = models.ForeignKey(Mnemonic)
    mnemonic_name = models.ForeignKey(Mnemonic, to_field="name")
    alert_message = models.CharField(max_length=200)
    
    red_high = models.FloatField()
    yellow_high = models.FloatField()
    yellow_low = models.FloatField()
    red_low = models.FloatField()



    

