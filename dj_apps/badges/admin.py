from django.contrib import admin

from .models import Badge


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "is_active",
        "sid",
        "created",
        "modified",
        "expiration",
        "owner",
    )
    list_filter = ("is_active", "created", "modified", "expiration", "owner")
