from django.db import models
from django.utils.text import slugify


class Slugable(models.Model):
    """To be used in conjunction with Namable mixin only"""

    class Meta:
        abstract = True

    slug = models.CharField(max_length=512, unique=True)

    # Remove if the slug should not be automatically created/modified
    def save(self, *args, **kwargs):
        if hasattr(self, "name"):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
