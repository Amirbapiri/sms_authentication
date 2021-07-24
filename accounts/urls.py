from django.urls import path

from accounts.views import panel, UserLoginView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("panel/", panel, name="panel")
]
