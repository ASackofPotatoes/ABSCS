from django.db import models
from django.db.models import Q, F
from dashboard.models import Mission
from page.models import Mnemonic

class Alarms(models.Model):    
    id = models.AutoField(primary_key=True)
    mission_id = models.ForeignKey(Mission, on_delete=models.CASCADE)
    mnemonic_id = models.ForeignKey(Mnemonic, on_delete=models.CASCADE)
    alert_message = models.CharField(max_length=200)
    
    red_high = models.FloatField(null=True)
    yellow_high = models.FloatField(null=True)
    yellow_low = models.FloatField(null=True)
    red_low = models.FloatField(null=True)
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(mission_id=Mnemonic(F("mnemonic_id").mission_id)),
                name="alarm_and_mnemonic_matching_mission"
            )
        ]


    

