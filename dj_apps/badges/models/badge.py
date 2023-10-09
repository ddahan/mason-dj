from django.conf import settings
from django.db import models

from core.mixins.deactivable import Deactivable, DeactivableQuerySet
from core.mixins.expirable import Expirable, ExpirableQueryset
from core.models.base_model import BaseModel, BaseQuerySet


class BaseBadgeQuerySet(ExpirableQueryset, DeactivableQuerySet, BaseQuerySet):
    def unowned(self):
        return self.filter(owner__isnull=True)

    def owned_by(self, owner):
        return self.filter(owner=owner)

    def vacants(self):
        """return badges that are available to be attached to a user"""
        return self.unowned().unexpired().order_by("identifier")

    def valids(self):
        """return all valid badges"""
        return self.unexpired().active()


class Badge(Expirable, Deactivable, BaseModel):
    class Meta:
        db_table = "tb_badges"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="propriétaire",
    )
