from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile


@receiver(signal=post_save, sender=User)
def create_profile_model(sender, instance, created, **kwargs):
    if created:
        profile_obj = Profile.objects.create(user=instance)
        return profile_obj
