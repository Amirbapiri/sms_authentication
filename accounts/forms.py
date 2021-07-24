from django import forms


class LoginForm(forms.Form):
    mobile = forms.CharField(max_length=11, required=True)
