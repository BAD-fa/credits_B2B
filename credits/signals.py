from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group

from .models import Supplier


@receiver(post_save, sender=Supplier)
def give_per_to_supplier(sender, instance, created, **kwargs):

    if created:
        suppliers_group = Group.objects.get(name='suppliers')
        suppliers_group.user_set.add(instance) 