from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# import debug_toolbar

urlpatterns = [
    # Django Admin dashboard
    path(f"{settings.PREFIX_URL_ADMIN}_admin/", admin.site.urls),
]
