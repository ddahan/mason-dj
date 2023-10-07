from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("dj_admin/", admin.site.urls),
]
