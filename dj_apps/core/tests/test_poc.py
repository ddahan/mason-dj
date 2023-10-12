from django.contrib.auth import get_user_model

import pytest

from badges.models.badge import Badge

User = get_user_model()


def test_a():
    assert 4 == 4


@pytest.mark.django_db
def test_my_user():
    badge = Badge.objects.create()
    print(badge.sid)
    assert Badge.objects.count() == 1


@pytest.mark.django_db
def test_my_user_2():
    badge = Badge.objects.create()
    print(badge.sid)
    assert Badge.objects.count() == 1
