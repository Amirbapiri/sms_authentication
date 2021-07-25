from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model, login
from django.views.generic import FormView

from accounts.forms import LoginForm, RegistrationForm, OTPVerificationForm
from accounts.utils import otp_random_generator, send_otp

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


class UserRegistrationView(FormView):
    template_name = "registration/signup.html"
    form_class = RegistrationForm

    def post(self, request, *args, **kwargs):
        try:
            mobile = request.POST.get("mobile")
            user = get_object_or_404(User, mobile=mobile)

            otp = otp_random_generator()
            send_otp(mobile, otp)

            user.otp = otp
            user.save()
            request.session['user_mobile'] = user.mobile
            return HttpResponseRedirect(reverse("accounts:otp_verification"))
        except Http404:
            signup_form = self.form_class(request.POST)
            if signup_form.is_valid():
                user = signup_form.save(commit=False)

                otp = otp_random_generator()
                send_otp(mobile, otp)

                user.otp = otp
                user.is_active = False
                user.save()
                request.session['user_mobile'] = user.mobile
                return HttpResponseRedirect(reverse("accounts:otp_verification"))
            return HttpResponseRedirect(reverse("accounts:signup"))


def verify_otp(request):
    mobile = request.session.get("user_mobile")
    if request.method == "POST":
        try:
            user = get_object_or_404(User, mobile=mobile)
            if not user.otp == int(request.POST.get("otp")):
                return HttpResponseRedirect(reverse("accounts:signup"))
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("accounts:panel"))
        except Http404:
            return HttpResponseRedirect(reverse("accounts:signup"))
    verification_form = OTPVerificationForm()
    return render(request, "registration/verify.html",
                  {"verification_form": verification_form, "user_mobile": mobile})


def panel(request):
    return render(request, "accounts/panel.html")
