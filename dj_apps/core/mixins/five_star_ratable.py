from django.core.validators import MaxValueValidator
from django.db import models


class FiveStarRatable(models.Model):
    class Meta:
        abstract = True

    rating = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])
