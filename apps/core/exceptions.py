class ProjectException(Exception):
    """
    Raise for specific exceptions related to this project.
    It should not be raised directly.
    """

    def __init__(self):
        if type(self) == ProjectException:
            raise Exception("<ProjectException> must be subclassed.")

    @property
    def slug(self):
        return type(self).__name__


class InconsistencyException(ProjectException):
    pass
