from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile, VerificationToken
from django.core.mail import send_mail
from django.template.loader import render_to_string


@receiver(signal=post_save, sender=User)
def create_profile_model(sender, instance, created, **kwargs):
    if created:
        profile_obj = Profile.objects.create(user=instance)
        return profile_obj


@receiver(signal=post_save, sender=Profile)
def email_verification_token(sender, instance, created, **kwargs):
    if created:
        obj = VerificationToken.objects.create(user=instance.user)
        msg_cont = {
            "token": obj.token
        }
        msg_html = render_to_string("Extras/confirmation.html", msg_cont)
        msg = "Please Confirm Your Account Now!"
        send_mail(
            subject="Confirmation Of Account",  
            from_email="djangoemailsafwan@gmail.com",
            message=msg, 
            recipient_list=["suhaibsafwan45@gmail.com"],
            html_message=msg_html
        )
        
        return obj
