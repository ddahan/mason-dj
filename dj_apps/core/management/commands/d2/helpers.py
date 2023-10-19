def indent(items: list[str], n: int = 2) -> list[str]:
    return [f"{' '*n}{item}" for item in items]


def add_label_and_properties(
    name: str, label: str | None = None, properties: list[str] | None = None
) -> list[str]:
    has_properties: bool = properties is not None and len(properties) > 0

    first_line = name
    if label or has_properties:
        first_line += ":"

    if label:
        first_line += f" {label}"

    if has_properties:
        first_line += " {"

    if properties and has_properties:
        return [first_line, *indent(properties), "}"]

    return [first_line]


def flatten(items: list[list[str]]) -> list[str]:
    return [item for sublist in items for item in sublist]


def app_model_display(dj_model) -> str:
    """Get a string formatted as <app_name>.<Model>
    This is used to describe D2 connections"""
    return f"{dj_model._meta.app_label}.{dj_model._meta.object_name}"
