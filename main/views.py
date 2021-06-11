from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import ForgotPasswordToken, Profile, ImageProfile
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .forms import ResetNewPasswordForm, UserForm, ForgotPasswordEmailForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied


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


def forgot_password_input_email(request):
    form = ForgotPasswordEmailForm()
    context = {}
    if request.method == "POST":
        form = ForgotPasswordEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user_obj = User.objects.get(email=email)
            qs = user_obj.forgot_token.filter(confirmed=False)
            token_obj = None
            if qs.exists():
                token_obj = qs.get()
            else:
                token_obj = user_obj.forgot_token.create(confirmed=False)
            
            messages.success(request, "Please Check your Account a Link has been sent...")
            context["token"] = token_obj

    context["form"] = form

    return render(request, "Accounts/forgot-password.html", context=context)


def create_new_password(request):
    context = {}
    token = request.GET.get("token")
    if token is None:
        raise Http404

    if request.user.is_authenticated:
        raise PermissionDenied
    
    qs = ForgotPasswordToken.objects.filter(token=token)
    if not qs.exists():
        raise Http404()

    obj = qs.get()
    if obj.confirmed == True:
        raise PermissionDenied

    form = ResetNewPasswordForm()
    
    if request.method == "POST":
        form = ResetNewPasswordForm(request.POST)
        if form.is_valid():
            form_user = obj.user
            password = form.cleaned_data.get("password1")
            form_user.set_password(password)
            form_user.save()
            obj.confirmed = True
            obj.save()

            return redirect("/")

    context["form"] = form

    return render(request, "Accounts/confirm-new-password.html", context)
