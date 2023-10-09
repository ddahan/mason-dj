from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from api.endpoints import api

urlpatterns = [
    # Ninja API
    path("api/", api.urls),
    # Django Admin dashboard
    path(f"{settings.PREFIX_URL_ADMIN}_admin/", admin.site.urls),
    # Django Debug Toolbar
    path("__debug__/", include("debug_toolbar.urls")),
]
