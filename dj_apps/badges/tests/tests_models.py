from django.contrib.auth import get_user_model

import pytest

from profiles.factories import UserFactory

from ..exceptions import BadgeAlreadyAssigned
from ..factories import BadgeFactory
from ..models.badge import Badge

User = get_user_model()


@pytest.fixture
def unassigned_badge(db) -> Badge:
    return BadgeFactory(owner=None)


@pytest.fixture
def assigned_badge(db) -> Badge:
    return BadgeFactory(owner=UserFactory())


def test_assign_when_unassigned(unassigned_badge: Badge):
    assert unassigned_badge.owner is None
    unassigned_badge.assign(UserFactory())
    assert unassigned_badge.owner is not None


def test_assign_when_assigned(assigned_badge: Badge):
    assert assigned_badge.owner is not None
    with pytest.raises(BadgeAlreadyAssigned):
        assigned_badge.assign(UserFactory())


def test_release_when_unassigned(unassigned_badge: Badge):
    assert unassigned_badge.owner is None
    unassigned_badge.release()
    assert unassigned_badge.owner is None


def test_release_when_assigned(assigned_badge: Badge):
    assert assigned_badge.owner is not None
    assigned_badge.release()
    assert assigned_badge.owner is None
