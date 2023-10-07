from django.db import models


class PriceField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs["max_digits"] = kwargs.get("max_digits", 10)
        kwargs["decimal_places"] = kwargs.get("decimal_places", 2)
        kwargs["default"] = kwargs.get("default", "0.00")
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is not None:
            return round(value, 2)
