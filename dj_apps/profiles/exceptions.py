from core.exceptions import ProjectException


class ProfilesException(ProjectException):
    pass


class EmailAlreadyExists(ProfilesException):
    pass


class InvalidLogin(ProfilesException):
    pass


class UnexistingUser(ProfilesException):
    pass
