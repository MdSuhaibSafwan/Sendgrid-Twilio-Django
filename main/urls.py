from . import views
from django.urls import path
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="User-Register-Page"),
    path("login/", LoginView.as_view(template_name="Accounts/login.html"), ),
    path("confirmation/", views.user_verified_signal_view, name="User-Account-Verify"),
    path("forgot-password/", views.forgot_password_input_email, name="Forgot-Password-Page"),
    path("forgot-password/confirm/new-password/", views.create_new_password, 
                                                            name="Create-New-Password-Page"),
]
