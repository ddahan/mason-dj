from typing import Literal


class ProjectException(Exception):
    """
    Raise for specific exceptions related to this project.
    """

    def __init__(
        self,
        message: str | None = None,
        error_level: Literal["global", "field"] | None = None,
        field_name: str | None = None,
    ):
        if type(self) == ProjectException:
            raise Exception("<ProjectException> must be subclassed.")

        if bool(field_name) != bool(error_level == "field"):
            raise Exception("field_name must be defined when error_level is field")

        self.message = message
        self.error_level = error_level
        self.field_name = field_name


class InconsistencyException(ProjectException):
    pass
