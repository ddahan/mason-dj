from typing import Iterable


class BuildContextException(Exception):
    """Raised when the given variable to build context is not found."""

    def __init__(self, unexisting_key):
        super().__init__(
            f"The variable {unexisting_key} doesn't exist in the locals dictionnary."
        )


def build_context(locals_dict: dict, *vars: Iterable[str]) -> dict:
    """Custom helper to build context from the given locals dict while staying DRY about
    the provided variables."""

    try:
        return {k: locals_dict[k] for k in vars}
    except KeyError as unexisting_key:
        raise BuildContextException(unexisting_key)
