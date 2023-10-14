"""
The conftest.py file in pytest is a configuration file that helps you set up some
fixtures that have a broader scope than just your test file. It's a way to provide a
consistent testing environment across multiple test files and test functions. You can
define fixtures, hooks, and plugins in this file.

"""

import pytest

from profiles.tests.factories import UserFactory
from token_auth.models.api_token import APIToken


@pytest.fixture()
def auth_headers(db) -> dict:
    # TODO: ensure it's called once per session to speed tests up
    user = UserFactory()
    token = APIToken.objects.get(user=user)
    headers = {"X-API-Key": token.key}
    return headers
