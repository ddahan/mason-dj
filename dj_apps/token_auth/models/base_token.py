from django.db import models

from core.mixins.time_stampable import TimeStampable


class BaseToken(TimeStampable, models.Model):
    """Child class must implement the primary_key field"""

    class Meta:
        abstract = True
