"""
These classes aim to add features to Django built-in Model / QuerySet.
This should be inherit from every model added to keep consistency.
"""

from django.db import models

from ..mixins.secret_id import SecretID
from ..mixins.time_stampable import TimeStampable, TimeStampableQueryset


class BaseQuerySet(TimeStampableQueryset, models.QuerySet):
    class Meta:
        abstract = True

    def ids(self):
        return self.values_list("id", flat=True)

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class BaseModel(SecretID, TimeStampable, models.Model):
    class Meta:
        abstract = True
