import orjson
from ninja.renderers import BaseRenderer


class ORJSONRenderer(BaseRenderer):
    """
    https://django-ninja.rest-framework.com/tutorial/response-renderers/
    """

    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data)
