import uuid

from django.db import models
from django.db.models.fields import UUIDField


class UUIDable(models.Model):
    class Meta:
        abstract = True

    uuid = UUIDField(db_index=True, default=uuid.uuid4, unique=True, editable=False)
