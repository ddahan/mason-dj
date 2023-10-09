from django.db.models import BooleanField, ExpressionWrapper, Q


def Condition(*args, **kwargs):
    """
    More here:
    https://www.django-antipatterns.com/pattern/annotate-a-condition-as-booleanfield.html
    """
    return ExpressionWrapper(Q(*args, **kwargs), output_field=BooleanField())
