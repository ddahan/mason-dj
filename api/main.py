from dataclasses import dataclass
from typing import Any

from django.http.response import Http404, HttpResponse

from ninja import NinjaAPI
from ninja.errors import ValidationError

from badges.endpoints import router as badges_router
from core.exceptions import ProjectException

from .authentication import ApiKeyAuth, InvalidToken
from .consts import BAD_REQUEST, NOT_FOUND, UNAUTHORIZED
from .renderers import ORJSONRenderer

api = NinjaAPI(title="Mason API", renderer=ORJSONRenderer(), auth=ApiKeyAuth())
api.add_router("badges", badges_router)

"""
Exception handling is handled here otherwise it's not taken into account
Potential exceptions default behaviour is overrided to get the same shape of response
no matter the type of error raised by the back-end:
* bad request
* object not found
* project error (expected potential error)
* unhandled error
"""


@dataclass
class ErrorContent:
    slug: str
    detail: Any = None

    def build_response(self, request, status) -> HttpResponse:
        return api.create_response(
            request,
            {"error": self.__dict__},
            status=status,
        )


@api.exception_handler(Http404)
def handle_not_found(request, _):
    return ErrorContent(NOT_FOUND, None).build_response(request, 404)


@api.exception_handler(ValidationError)
def handle_bad_request(request, e):
    return ErrorContent(BAD_REQUEST, e.errors).build_response(request, 400)


@api.exception_handler(InvalidToken)
def handle_invalid_token(request, _):
    return ErrorContent(UNAUTHORIZED, None).build_response(request, 401)


@api.exception_handler(ProjectException)
def handle_project_error(request, e):
    return ErrorContent(e.slug, None).build_response(request, 400)


# @api.exception_handler(Exception)
# def handle_exception(request, _):
#     return ErrorContent(UNKNOWN_ERROR, None).build_response(request, 500)
