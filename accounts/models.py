from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    # We're creating a private method with only needed fields to call it within
    # the 'create_user'
    def _create_user(self, mobile, **extra_fields):
        if not mobile:
            raise ValueError('The given mobile phone must be set')
        user = self.model(mobile=mobile, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, mobile, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        return self._create_user(mobile, **extra_fields)

    def create_superuser(self, mobile, **extra_fields):
        # This method uses the same method as 'create_user' did. However we must set
        # some extra information in the extra_fields to apply it to the model instance.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile, **extra_fields)


class User(AbstractUser):
    # We don't want to include 'username' in our migrations so we do override it.
    username = None
    mobile = models.CharField(max_length=11, unique=True)
    otp = models.PositiveIntegerField(blank=True, null=True)
    otp_create_time = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.mobile)
