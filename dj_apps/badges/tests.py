from django.contrib.auth import get_user_model

import pytest

from badges.models.badge import Badge

User = get_user_model()


@pytest.fixture
def badge_1(db) -> Badge:
    return Badge.objects.create(sid="12345678")


def test_easy():
    assert 4 == 4


def test_my_user(db, badge_1):
    assert badge_1.sid == "12345678"


def test_my_user_2(db, badge_1):
    assert badge_1.sid == "12345678"
