from typing import Any, Optional

from django.http.request import HttpRequest

from ninja.security import APIKeyHeader

from token_auth.models import APIToken


class InvalidToken(Exception):
    pass


class ApiKeyAuth(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request: HttpRequest, key: Optional[str]) -> Optional[Any]:
        try:
            user = APIToken.objects.get(key=key).user
        except APIToken.DoesNotExist:
            raise InvalidToken  # will allow a custom 401 exception
        else:
            # NOTE: we could log api usage here
            return user
