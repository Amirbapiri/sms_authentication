from django.http import Http404
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


class MobileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        The authenticate method takes a request argument
        and credentials as keyword arguments.

        This method authenticates against mobile phone
        """
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = get_object_or_404(User, mobile=username)
        except User.DoesNotExist:
            return None
        return user

    def get_user(self, user_id):
        try:
            return get_object_or_404(User, pk=user_id)
        except User.DoesNotExist:
            return None
