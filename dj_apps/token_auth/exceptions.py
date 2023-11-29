from core.exceptions import ProjectException


class TokenAuthException(ProjectException):
    pass


class MagicLinkNotFound(TokenAuthException):
    message = "The given token does not exist. It may have already been used."
