from django.db.models.signals import post_migrate
from django.dispatch import receiver
from page.models import Mnemonic


@receiver(post_migrate)
def create_default_mnemonic(sender, **kwargs):
    if not Mnemonic.objects.filter(id=0).exists():
        null = Mnemonic.objects.create(
            type="null",
            name="null",
            value="null",
            unit="null",
            id=0
        )
        null.save()
