from django.db import models


class UneditableException(ValueError):
    pass


class Uneditable(models.Model):
    """Mixin to prevent an object to be changed.
    It is just for the save() method, not the delete one.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise UneditableException
        super().save(*args, **kwargs)


class UneditSetable(models.Model):
    """Same that Uneditable except it is only active when editable field is False"""

    class Meta:
        abstract = True

    editable = models.BooleanField(default=True, verbose_name="éditable")

    def make_uneditable(self, *args, **kwargs):
        if self.editable:
            self.editable = False
            super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self._state.adding and not self.editable:
            raise UneditableException
        super().save(*args, **kwargs)
