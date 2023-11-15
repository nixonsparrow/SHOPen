from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Item


@receiver(post_save, sender=Item)
def manager_create_dirty_points(sender, instance, created, **kwargs):
    if created:
        instance.product.quantity -= instance.quantity
        instance.product.save()
