from core.exceptions import ProjectException


class ProfilesException(ProjectException):
    pass


class EmailAlreadyExists(ProjectException):
    pass


class InvalidLogin(ProjectException):
    pass
