import random
import secrets
import string
from typing import Sequence


def get_secret_id() -> str:
    """
    Wrapper to python built-in method to be used as a callable, while ensuring
    nbytes is defined to get the same string length in output.
    nbytes == 16 means a better entropy than uuid4
    """
    return secrets.token_urlsafe(nbytes=16)


def make_random_str(size: int, chars: str = string.printable) -> str:
    """
    Build a random string of `size`, using `chars`
    """
    return "".join(random.choice(chars) for _ in range(size))


def shorten_str(msg: str, max_size) -> str:
    """
    Shorten the `msg` max size
    """
    if not len(msg) > max_size > 0:
        raise ValueError("max_size should be positive and inferior to message length")
    return f"{msg[:max_size]}…"


def first_upper(s: str) -> str:
    """
    Return first letter in uppercase. Differs from capitalize that removes all uppercases
    letters in the string
    """
    return s[:1].upper() + s[1:]


def get_format_arguments(s: str) -> bool:
    """
    Return names of all format argument of the given string
    🔗 https://stackoverflow.com/a/46161774/2255491
    """
    return [tup[1] for tup in string.Formatter().parse(s) if tup[1] is not None]


def to_joined_str(seq: Sequence, char=",") -> str:
    return char.join(seq)
