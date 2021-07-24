from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login
from django.views.generic import FormView

from accounts.forms import LoginForm

User = get_user_model()


class UserLoginView(FormView):
    template_name = "registration/login.html"
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        login_form = self.form_class(request.POST)
        if login_form.is_valid():
            user = get_object_or_404(User, **login_form.cleaned_data)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("accounts:panel"))
            return HttpResponseRedirect(reverse("accounts:login"))
        return HttpResponseRedirect(reverse("accounts:login"))


def panel(request):
    return render(request, "accounts/panel.html")
