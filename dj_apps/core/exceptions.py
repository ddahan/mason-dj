from typing import Literal

from django.core.exceptions import ImproperlyConfigured


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
        error_level: Literal["global", "non_field", "field"] = "global",
        field_name: str | None = None,
    ):
        if type(self) == ProjectException:
            raise Exception("<ProjectException> must be subclassed.")

        if bool(field_name) != (error_level == "field"):
            raise Exception("field_name must be defined when error_level is 'field'")

        # Use default exception message if it exists, otherwise, rely on an initialiation
        if message:
            self.message = message
        else:
            if not self.message:
                raise ImproperlyConfigured(
                    "No message is given at all. Please provide a message in the exception itself, or in the endpoint."
                )
            # This might seem an error, but what this line does is essentially take the message from the class level (if it exists) and creates an instance-level attribute with the same value. This ensures that message is in the instance's __dict__. If this line is removed and no message is passed during initialization, there won't be an instance attribute message created. The message will still be accessible through the class, but it won't appear in the instance's __dict__ because __dict__ only shows attributes set at the instance level.
            self.message = self.message

        self.error_level = error_level
        self.field_name = field_name


class InconsistencyException(ProjectException):
    pass
