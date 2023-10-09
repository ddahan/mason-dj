def to_int_or_none(s: str) -> int | None:
    """
    Try to cast s as int and return it, or return None if it's impossible
    """
    try:
        return int(s)
    except ValueError:
        return None
