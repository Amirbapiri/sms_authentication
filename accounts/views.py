from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model, login
from django.views.generic import FormView
from django.contrib import messages

from accounts.forms import LoginForm, RegistrationForm, OTPVerificationForm
from accounts.utils import otp_random_generator, send_otp, is_expired
from django.contrib.auth.decorators import login_required

User = get_user_model()


class UserLoginView(FormView):
    template_name = "registration/login.html"
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        login_form = self.form_class(request.POST)
        if login_form.is_valid():
            try:
                user = get_object_or_404(User, **login_form.cleaned_data)
                otp = otp_random_generator()
                send_otp(user.mobile, otp)
                user.otp = otp
                user.save()

                login(request, user)
                return HttpResponseRedirect(reverse("accounts:otp_verification"))
            except Http404:
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
            return HttpResponseRedirect(reverse("accounts:otp_verification"))
        except Http404:
            signup_form = self.form_class(request.POST)
            if signup_form.is_valid():
                user = signup_form.save(commit=False)

                otp = otp_random_generator()
                send_otp(user.mobile, otp)

                user.otp = otp
                user.is_active = False
                user.save()
                return HttpResponseRedirect(reverse("accounts:otp_verification"))
            return HttpResponseRedirect(reverse("accounts:signup"))


def verify_otp(request):
    user = get_object_or_404(User, mobile=request.user)
    if request.method == "POST":
        try:
            # Check if otp has been expired or not
            if is_expired(user.mobile):
                messages.add_message(request, messages.ERROR, "OTP has been expired, try again!")
                return HttpResponseRedirect(reverse("accounts:signup"))
            if not user.otp == int(request.POST.get("otp")):
                messages.add_message(request, messages.ERROR, "OTP is incorrect.")
                return HttpResponseRedirect(reverse("accounts:otp_verification"))
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("accounts:panel"))
        except Http404:
            messages.add_message(request, messages.ERROR, "Oops! Something went wrong!")
            return HttpResponseRedirect(reverse("accounts:signup"))
    verification_form = OTPVerificationForm()
    return render(request, "registration/verify.html",
                  {"verification_form": verification_form, "user_mobile": user.mobile})


def panel(request):
    return render(request, "accounts/panel.html")
