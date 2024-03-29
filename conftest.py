"""
The conftest.py file in pytest is a configuration file that helps you set up some
fixtures that have a broader scope than just your test file. It's a way to provide a
consistent testing environment across multiple test files and test functions. You can
define fixtures, hooks, and plugins in this file.

"""

import pytest

from profiles.factories import UserFactory
from token_auth.models.api_token import APIAccessToken


@pytest.fixture()
def auth_headers(db) -> dict:
    # TODO: ensure it's called once per session to speed tests up
    user = UserFactory()
    token = APIAccessToken.objects.create(user=user)
    headers = {"X-API-Key": token.key}
    return headers
