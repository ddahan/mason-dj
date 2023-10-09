from decimal import Decimal
from typing import Sequence

from .string_utils import first_upper


def as_percentage(number: Decimal) -> str:
    """
    Return a percentage display with no truncating
    """
    return f"{float(number) * 100} %".replace(".", ",")


def as_integer_percentage(number: Decimal | float) -> str:
    """
    Return a percentage truncated to an int. For example:
    - 0.05 will return "5 %"
    - 0.051 witll return "5 %" too
    The purpose is to display percentages without commas.
    It should be used on number that have 2 decimal places max, to avoid any undesired
    rounding.
    """
    return f"{int(number * 100)} %"


def as_price(number: Decimal | float) -> str:
    """
    Note that we don't round to 2 digits since we expect number to be recorded with 2
    digits after coma in database.
    When possible, we should use template methods instead of this!
    """
    return f"{number} €".replace(".", ",")


def verbose_display(model_class, field_name: str = None, cap=True) -> str:
    """
    Return the verbose name of a class field if provided, or the class name if field
    is not provided. The result can be capitalized or not.
    """
    if field_name:
        lower_result = model_class._meta.get_field(field_name).verbose_name
    else:
        lower_result = model_class._meta.verbose_name

    return first_upper(lower_result) if cap else lower_result


def as_comma_seperated(fields: Sequence[str]) -> str:
    """
    Return the sequence as a string, separated by commas.
    """
    return ", ".join(fields)


def auto_plural(quantity, field_name, field_name_plural=None):
    if quantity < 2:
        return f"{quantity} {field_name}"
    else:
        if not field_name_plural:
            field_name_plural = field_name + "s"
        return f"{quantity} {field_name_plural}"
