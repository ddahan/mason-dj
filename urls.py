from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from api.main import api

urlpatterns = [
    # Home page (redirects to API doc as there is no home)
    path("", lambda request: redirect("api/docs")),
    # API
    path("api/", api.urls),
    # Django Admin dashboard
    path(f"{settings.PREFIX_URL_ADMIN}_admin/", admin.site.urls),
    # Django Debug Toolbar
    path("__debug__/", include("debug_toolbar.urls")),
]
