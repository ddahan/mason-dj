from core.utils.testing_utils import same_items
from profiles.tests.factories import UserFactory

from ..models.badge import Badge
from .factories import BadgeFactory, ExpiredBadgeFactory, UnexpiredBadgeFactory


def test_unassigned_and_assigned_to(db):
    user_1 = UserFactory()
    b1 = BadgeFactory(owner=user_1)
    BadgeFactory(owner=UserFactory())
    b3 = BadgeFactory(owner=None)

    assert same_items(Badge.objects.unassigned(), [b3])
    assert same_items(Badge.objects.assigned_to(user_1), [b1])


def test_vacants(db):
    ExpiredBadgeFactory(owner=UserFactory())
    ExpiredBadgeFactory(owner=None)
    UnexpiredBadgeFactory(owner=UserFactory())
    b4 = UnexpiredBadgeFactory(owner=None)

    assert same_items(Badge.objects.vacants(), [b4])


def test_valids(db):
    ExpiredBadgeFactory(is_active=True)
    ExpiredBadgeFactory(is_active=False)
    b3 = UnexpiredBadgeFactory(is_active=True)
    UnexpiredBadgeFactory(is_active=False)

    assert same_items(Badge.objects.valids(), [b3])
