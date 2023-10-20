from django.contrib import admin

from .models.badge import Badge


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = (
        "identifier",
        "is_active",
        "expiration",
        "owner",
    )
    list_filter = ("is_active", "created", "expiration", "owner")
