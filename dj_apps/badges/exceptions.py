from core.exceptions import ProjectException


class BadgesException(ProjectException):
    pass


class BadgeAlreadyAssigned(BadgesException):
    error_level = "global"
    message = "This badge has already been assigned."
