from django.db.models.signals import post_migrate
from django.dispatch import receiver
from page.models import Mnemonic
from django.core.cache import cache


#@receiver(post_migrate)
#def create_default_mnemonic(sender, **kwargs):
    #current_mission = cache.get("current_misison")
    #if not Mnemonic.objects.using(current_mission).filter(id=0).exists():
        #null = Mnemonic.objects.using(current_mission).create(
            #type="null",
            #name="null",
            #value="null",
            #unit="null",
            #id=0
        #)
        #null.save()
#