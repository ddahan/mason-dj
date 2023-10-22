from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

"""
Django built-in Permission system is tightly coupled with particular models.
But some actions may not be related to particular model (eg. access section in the app).
We could rewrite a whole permission system, but we'd lose all Django benefits 
(@permission_required, User.has_perm, etc.)
The purpose of this snippet is to create a Permission type than can be used completely
unrelated to any model.

# https://stackoverflow.com/questions/13932774/
# how-can-i-use-django-permissions-without-defining-a-content-type-or-model

"""


class GlobalPermissionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(content_type__model="global_permission")


class GlobalPermission(Permission):
    objects = GlobalPermissionManager()

    class Meta:
        proxy = True
        verbose_name = "global_permission"

    def save(self, *args, **kwargs):
        # This will give "global_permission" dummy `ContentType` value to
        # this permission.
        content_type, created = ContentType.objects.get_or_create(
            model=self._meta.verbose_name,
            app_label=self._meta.app_label,
        )
        self.content_type = content_type
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
