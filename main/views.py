from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Profile, ImageProfile
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .forms import UserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist


def is_account_verified(request):
    profile = request.user.profile
    if profile.verified == True:
        return True

    return False


class UserRegisterView(CreateView):
    form_class = UserForm
    template_name = "accounts/register.html"
    success_url = "/"

    def form_valid(self, form):
        messages.success(self.request, "Thanks For Registering")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        print(username, password)
        self.object = form.save()

        user_auth = authenticate(self.request, username=username, password=password)
        if user_auth:
            login(self.request, user_auth)
            print("Logged In")

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            raise Http404

        return context


@login_required
def user_verified_signal_view(request):
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        raise Http404

    if profile.verified == True:
        raise Http404
        
    token = request.GET.get("token")    
    if token is None:
        raise Http404
        
    user = request.user
    qs = user.verification_token.filter(token=token)
    if not qs.exists():
        raise Http404()

    qs = qs.filter(verified=False)
    if not qs.exists():
        raise Http404()

    obj = qs.get()
    obj.verified = True
    obj.save()

    profile.verified = True
    profile.save()

    messages.success(request, "Your Account Has been Verified Thank you...")
    return redirect("/")
