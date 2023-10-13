from typing import Iterable


def same_items(*iterables: Iterable) -> bool:
    """Return True if all given iterables contain the same quantity of the same elements,
    no matter the order."""

    # Preliminary checks
    if len(iterables) < 2:
        raise ValueError("At least two iterables must be provided")

    if not all([isinstance(it, Iterable) for it in iterables]):
        raise TypeError("All given parameters must be iterable")

    # Convert the first iterable to a sorted list
    first_sorted = sorted(list(iterables[0]))

    # Compare the first sorted list with the rest of the iterables
    return all(sorted(list(it)) == first_sorted for it in iterables[1:])
