from django.contrib import admin
from .models import Profile, ImageProfile, VerificationToken, ForgotPasswordToken


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "verified", "date_created", "time_created", "last_updated"]


class ImageProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "date_created", "time_created", "last_updated"]


class VerificationTokenAdmin(admin.ModelAdmin):
    list_display = ["user", "token", "verified", "date_created", "time_created", "last_updated"]
    

class ForgotTokenAdmin(admin.ModelAdmin):
    list_display = ["user", "token", "confirmed", "date_created", "time_created", "last_updated"]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(ImageProfile, ImageProfileAdmin)
admin.site.register(VerificationToken, VerificationTokenAdmin)
admin.site.register(ForgotPasswordToken, ForgotTokenAdmin)
