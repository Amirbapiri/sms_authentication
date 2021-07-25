from django.urls import path

from accounts.views import (
    panel,
    UserLoginView,
    UserRegistrationView,
    verify_otp
)

urlpatterns = [
    path("signup/", UserRegistrationView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("verification/", verify_otp, name="otp_verification"),
    path("panel/", panel, name="panel")
]
