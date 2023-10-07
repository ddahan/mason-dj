from django.db import models


class AutoValidable(models.Model):
    """
    Will force the validation process on save.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
