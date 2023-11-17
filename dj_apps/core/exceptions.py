from typing import Literal


class ProjectException(Exception):
    """
    Raise for specific exceptions related to this project.
    Additional data can be binded to allow front-end to deal with the exception.
    Parameters:
    * message: the message which should be displayed
    * error_level: to know how to display the error: globally in a toast, or locally
    * field_name: if error_level is field, provide the field name
    """

    def __init__(
        self,
        message: str | None = None,
        error_level: Literal["global", "field"] | None = None,
        field_name: str | None = None,
    ):
        if type(self) == ProjectException:
            raise Exception("<ProjectException> must be subclassed.")

        if bool(field_name) != (error_level == "field"):
            raise Exception("field_name must be defined when error_level is field")

        self.message = message
        self.error_level = error_level
        self.field_name = field_name


class InconsistencyException(ProjectException):
    pass
