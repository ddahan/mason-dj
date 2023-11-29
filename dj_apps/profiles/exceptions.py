from core.exceptions import ProjectException


class ProfilesException(ProjectException):
    pass


class EmailAlreadyExists(ProfilesException):
    message = "This email already exists."
    error_level = "field"
    field_name = "email"


class InvalidLogin(ProfilesException):
    message = "Wrong given credentials. Please try again."
    error_level = "non_field"


class UnexistingUser(ProfilesException):
    message = "This user does not exist in our database."
    error_level = "field"
    field_name = "email"
