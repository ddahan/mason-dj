from django.db import models


class Namable(models.Model):
    """if no __str__ method is defined in the child class, the name is returned"""

    class Meta:
        abstract = True

    name = models.CharField(max_length=512, unique=True)

    def __str__(self) -> str:
        return self.name
