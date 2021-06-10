from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from random import choice
from string import ascii_letters
from django.conf import settings

User = settings.AUTH_USER_MODEL


def create_random_slug(number=8):
    return "".join(choice(ascii_letters) for i in range(number))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    verified = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    time_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}| Profile."


class ImageProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="image")
    image = models.ImageField(upload_to="user-images")    
    date_created = models.DateField(auto_now_add=True)
    time_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}| Profile-Image."

