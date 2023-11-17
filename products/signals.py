from django.db.models.signals import post_save
from django.dispatch import receiver
import apscheduler

from .models import Item


@receiver(post_save, sender=Item)
def subtract_quantity(sender, instance, created, **kwargs):
    if created:
        instance.product.quantity -= instance.quantity
        instance.product.save(update_fields=["quantity"])
