from django.contrib import admin

from .models import MailSkeleton


@admin.register(MailSkeleton)
class MailSkeletonAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "subject", "send_mode")
