from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile, VerificationToken


@receiver(signal=post_save, sender=User)
def create_profile_model(sender, instance, created, **kwargs):
    if created:
        profile_obj = Profile.objects.create(user=instance)
        return profile_obj


@receiver(signal=post_save, sender=Profile)
def email_verification_token(sender, instance, created, **kwargs):
    if created:
        obj = VerificationToken.objects.create(user=instance.user)
        return obj
