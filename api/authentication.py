from typing import Any

from django.http.request import HttpRequest

from ninja.security import APIKeyHeader

from token_auth.models import APIAccessToken


class InvalidToken(Exception):
    pass


class ApiKeyAuth(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request: HttpRequest, key: str | None) -> Any:
        user = APIAccessToken.challenge(key)
        if user:
            return user
        else:
            raise InvalidToken  # will allow a custom 401 exception
