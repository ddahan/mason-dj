from typing import Literal


class ProjectException(Exception):
    """
    Raise for specific exceptions related to this project.
    Additional data can be binded to allow front-end to deal with the exception.

    Parameters:
    * message: the message which should be displayed
    * error_level: to know how to display the error:
        - 'global' -> in a toast
        - 'non_field' -> at the top of the form
        - 'field' -> on a specific field
    * field_name: if error_level is 'field', provide the field name

    Note that every exception can be overrided when instanciated. This can be handful to adapt the error the context.

    """

    def __init__(
        self,
        message: str | None = None,
        error_level: Literal["global", "non_field", "field"] = None,
        field_name: str | None = None,
    ):
        if self.__class__.__subclasses__():
            raise NotImplementedError(
                f"{self.__class__.__name__} should not be instanciated directly."
            )

        # Define attributes from class definition or object instanciation
        for attr_name, attr_value in {
            "message": message,
            "error_level": error_level,
            "field_name": field_name,
        }.items():
            setattr(
                self,
                attr_name,
                attr_value
                if attr_value is not None
                else getattr(self.__class__, attr_name, None),
            )

        # Verification Checks
        if not self.message or not self.error_level:
            raise InconsistencyException(
                "A 'message' and an 'error_level' must be defined, either in class definition, either in object instanciation."
            )

        if bool(self.error_level == "field") != bool(self.field_name):
            raise InconsistencyException(
                "'field_name' must be defined when error_level is 'field'"
            )


class InconsistencyException(Exception):
    pass
