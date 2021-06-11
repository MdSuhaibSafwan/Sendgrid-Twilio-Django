from . import views
from django.urls import path

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="User-Register-Page"),
    path("confirmation/", views.user_verified_signal_view, name="User-Account-Verify"),
]
