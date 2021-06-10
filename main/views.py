from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile, ImageProfile
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .forms import UserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import Http404


class UserRegisterView(CreateView):
    form_class = UserForm
    template_name = "user/register.html"

    def form_valid(self, form):
        messages.success(self.request, "Thanks For Registering")
        return super().form_valid(form=form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            raise Http404
            
        return context

