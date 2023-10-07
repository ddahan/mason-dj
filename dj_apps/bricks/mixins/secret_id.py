from django.db import models

from utils.string_utils import get_secret_id


class SecretID(models.Model):
    """Allow any objet to have a second id, which is harder to guess and do not provide
    indication about the other objects in database. This is can be used for lookup.
    """

    class Meta:
        abstract = True

    sid = models.CharField(
        unique=True,
        db_index=True,
        default=get_secret_id,
        max_length=128,
        editable=False,
    )
