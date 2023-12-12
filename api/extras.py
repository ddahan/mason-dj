"""
Copied utilities from django-ninja-extra
https://eadwincode.github.io/django-ninja-extra/
"""

from typing import no_type_check

from ninja.types import TCallable

##########################################################################################
# shortcuts
##########################################################################################


@no_type_check
def add_ninja_contribute_args(func: TCallable, value: tuple) -> None:
    _ninja_contribute_args: list[tuple] = getattr(func, "_ninja_contribute_args", [])
    assert isinstance(_ninja_contribute_args, list)
    _ninja_contribute_args.append(value)
    func._ninja_contribute_args = _ninja_contribute_args
