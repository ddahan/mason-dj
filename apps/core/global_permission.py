from typing import Any

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

# https://stackoverflow.com/questions/13932774/
# how-can-i-use-django-permissions-without-defining-a-content-type-or-model


class GlobalPermissionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(content_type__model="global_permission")


class GlobalPermission(Permission):
    """
    A global permission, not attached to a specific model
    """

    # TODO: get unit test from fugo

    objects: Any = GlobalPermissionManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        ct, created = ContentType.objects.get_or_create(
            model=self._meta.verbose_name,
            app_label=self._meta.app_label,
        )
        self.content_type = ct
        super(GlobalPermission, self).save(*args)
