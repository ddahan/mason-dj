from core.exceptions import ProjectException


class MailSlugNotFound(ProjectException):
    message = "The provided slug does not match with any email"
