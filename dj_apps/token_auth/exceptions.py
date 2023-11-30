from core.exceptions import ProjectException


class TokenAuthException(ProjectException):
    pass


class MagicLinkNotFound(TokenAuthException):
    message = "The given token does not exist or may have already been used."
    error_level = "global"


class CodeNotFound(TokenAuthException):
    message = "The entered code is wrong or may have already been used."
    error_level = "field"
    field_name = "code"
