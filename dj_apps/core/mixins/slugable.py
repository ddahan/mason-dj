from django.db import models


class Slugable(models.Model):
    """To be used in conjunction with Namable mixin only"""

    class Meta:
        abstract = True

    slug = models.CharField(max_length=512, unique=True)

    # Uncomment if the slug should be automatically modified
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)
