from django.db import models


class ToolableQuerySet(models.QuerySet):
    """Add additional tools to any queryset"""

    class Meta:
        abstract = True

    def ids(self):
        return self.values_list("id", flat=True)

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
