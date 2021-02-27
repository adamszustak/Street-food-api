from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Truck


@receiver(post_save, sender=Truck)
def postmodel_post_delete_handler(sender, **kwargs):
    cache.clear()
