from django.db.models import Value
from django.db.models.functions import Coalesce


def zero(stuff):
    """
    Prevent an aggregate Sum() from returning None
    https://docs.djangoproject.com/en/dev/ref/models/database-functions/#coalesce
    """

    return Coalesce(stuff, Value(0))
