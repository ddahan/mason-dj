from django.db import models

from positions import PositionField


class Positionable(models.Model):
    class Meta:
        abstract = True

    position = PositionField()
