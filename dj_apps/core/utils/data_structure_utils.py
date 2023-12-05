from functools import reduce
from typing import Iterable


def as_dict(o, skip_empty=False):
    """
    Transform a structure like a dataclass to a dict, providing the ability to ignore
    None values. Can be use to transmit object descriptions to an API
    """
    return {k: v for k, v in o.__dict__.items() if not (skip_empty and v is None)}


def recursive_getattr(obj, attr, *args):
    """
    Recursive getattr that cross relationships.
    More here: https://stackoverflow.com/a/31174427/2255491
    """

    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return reduce(_getattr, [obj] + attr.split("."))


def remove_keys(dico: dict, keys: str | Iterable) -> dict:
    """Return a new dict without the given key(s)."""
    if isinstance(keys, str):
        keys = [keys]
    return {k: v for k, v in dico.items() if k not in keys}
