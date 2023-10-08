from core.exceptions import ProjectException


class BadgesException(ProjectException):
    pass


class BadgeNotUnique(BadgesException):
    pass


class BadgeAlreadyAssigned(BadgesException):
    pass


class InvalidBadge(BadgesException):
    pass


class BadgeNoOwner(BadgesException):
    pass


class BadgeBadProfile(BadgesException):
    pass
