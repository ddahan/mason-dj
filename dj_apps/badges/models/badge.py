from django.conf import settings
from django.db import models

from core.mixins.deactivable import Deactivable, DeactivableQuerySet
from core.mixins.expirable import Expirable, ExpirableQueryset
from core.models.base_model import BaseModel, BaseQuerySet

from ..exceptions import BadgeAlreadyAssigned


class BadgeQuerySet(ExpirableQueryset, DeactivableQuerySet, BaseQuerySet):
    def unassigned(self):
        return self.filter(owner__isnull=True)

    def assigned_to(self, owner):
        return self.filter(owner=owner)

    def vacants(self):
        return self.unassigned().unexpired()

    def valids(self):
        return self.unexpired().active()


class Badge(Expirable, Deactivable, BaseModel):
    class Meta:
        db_table = "tb_badges"

    objects = models.Manager.from_queryset(BadgeQuerySet)()

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="propriétaire",
    )

    def assign(self, user):
        """Assign a badge to a user. Raise an error if already assigned."""
        if self.owner:
            raise BadgeAlreadyAssigned
        self.owner = user
        self.save()

    def release(self):
        """Release a badge. Raise no error if already released."""
        self.owner = None
        self.save()

    def __str__(self):
        return self.sid
