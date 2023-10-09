import string

from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

from core.utils.string_utils import make_random_str
from core.validators import NumericValidator


class Digit6KeyMixin(models.Model):
    class Meta:
        abstract = True

    key = models.CharField(
        max_length=6,
        validators=[MinLengthValidator(6), MaxLengthValidator(6), NumericValidator],
    )

    def _build_key(self, size=6) -> str:
        return make_random_str(size, chars=string.digits)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.key = self._build_key()
        super().save(*args, **kwargs)
