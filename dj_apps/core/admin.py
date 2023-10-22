from django.contrib import admin

from .global_permission import GlobalPermission
from .models.app_parameters import AppParameters


@admin.register(GlobalPermission)
class GlobalPermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "codename")
    exclude = ("content_type",)


admin.site.register(AppParameters)
