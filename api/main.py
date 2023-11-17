from django.core.exceptions import ValidationError as DjangoValidationError
from django.http.response import Http404

from ninja import NinjaAPI
from ninja.errors import ValidationError as NinjaValidationError

from badges.endpoints import router as badges_router
from core.exceptions import ProjectException
from token_auth.endpoints import router as auth_router

from .authentication import ApiKeyAuth, InvalidToken
from .renderers import ORJSONRenderer

api = NinjaAPI(
    title="Mason API",
    renderer=ORJSONRenderer(),
    auth=ApiKeyAuth(),
    urls_namespace="api",
)

# Add routers here
api.add_router("badges", badges_router)
api.add_router("auth", auth_router)

"""
Exception handling is handled here otherwise it's not taken into account
Potential exceptions default behaviour is overrided to get the same shape of response
no matter the type of error raised by the back-end:
* bad request
* object not found
* project error (expected potential error)
* unhandled error
"""


# TODO: Unit tests to see if we got the same output for all errors, with all data in it


@api.exception_handler(Http404)
def handle_not_found(request, _):
    return api.create_response(
        request,
        dict(message="The requested resource has not been found.", error_level="global"),
        status=404,
    )


@api.exception_handler(DjangoValidationError)
def handle_bad_request(request, e):
    return api.create_response(
        request,
        dict(message="The request is not correctly formatted.", error_level="global"),
        status=400,
    )


@api.exception_handler(NinjaValidationError)
def handle_bad_request_ninja(request, _):
    return api.create_response(
        request,
        dict(message="The request is not correctly formatted.", error_level="global"),
        status=400,
    )


@api.exception_handler(InvalidToken)
def handle_invalid_token(request, _):
    return api.create_response(
        request,
        dict(
            message="You are not authorized to perform this operation.",
            error_level="global",
        ),
        status=401,
    )


@api.exception_handler(ProjectException)
def handle_project_error(request, e):
    return api.create_response(
        request,
        e.__dict__,
        status=400,
    )


@api.exception_handler(Exception)
def handle_exception(request, _):
    return api.create_response(
        request,
        dict(message="An unknown servor error has occurred.", error_level="global"),
        status=500,
    )
