from django.conf import settings
from django.db import models

from safedelete import SOFT_DELETE
from safedelete.managers import SafeDeleteManager
from safedelete.models import SafeDeleteModel
from safedelete.queryset import SafeDeleteQueryset

from core.mixins.auto_validable import AutoValidable
from core.mixins.deactivable import Deactivable, DeactivableQuerySet
from core.mixins.expirable import Expirable, ExpirableQueryset
from core.mixins.time_stampable import TimeStampable
from core.utils.string_utils import get_secret_id

from ..exceptions import BadgeAlreadyAssigned


class BadgeQuerySet(ExpirableQueryset, DeactivableQuerySet, SafeDeleteQueryset):
    def unassigned(self):
        return self.filter(owner__isnull=True)

    def assigned_to(self, owner):
        return self.filter(owner=owner)

    def vacants(self):
        return self.unassigned().unexpired()

    def valids(self):
        return self.unexpired().active()


class Badge(Expirable, Deactivable, TimeStampable, AutoValidable, SafeDeleteModel):
    class Meta:
        db_table = "tb_badges"

    objects = SafeDeleteManager.from_queryset(BadgeQuerySet)()
    _safedelete_policy = SOFT_DELETE

    identifier = models.CharField(
        max_length=2048,
        unique=True,
        default=get_secret_id,
        editable=False,
        verbose_name="identifiant",
    )

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
        return self.identifier
