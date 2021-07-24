from django.contrib import admin
from django.urls import path, include

from accounts import urls as account_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    # accounts
    path("accounts/", include((account_urls, "accounts"), namespace="accounts")),
]
