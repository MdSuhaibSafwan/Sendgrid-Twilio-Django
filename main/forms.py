from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, ImageProfile
from django.utils.translation import gettext, gettext_lazy as _


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is Already connected to other User.")

        return email


class ForgotPasswordEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            return email

        raise forms.ValidationError("Email is Already connected to other User.")


class ResetNewPasswordForm(forms.Form):
    password1 = forms.CharField(
        label=_("password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="Please Provide a good Password..."
    )
    
    password2 = forms.CharField(
        label=_("Password Confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="Enter The Same Password As Before..."
    )

    def clean_password2(self):
        ps1 = self.cleaned_data.get("password1")
        ps2 = self.cleaned_data.get("password2")
        if ps1 and ps2:
            if ps1 == ps2:
                return ps2
            raise forms.ValidationError("The Two Password Field Did not Match...", code="400")
        raise forms.ValidationError("Please Provide both the Password", code="403")
