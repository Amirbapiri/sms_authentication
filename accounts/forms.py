from django import forms
from django.contrib.auth import get_user_model


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("mobile",)


class LoginForm(forms.Form):
    mobile = forms.CharField(max_length=11, required=True)


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=5, required=True)
