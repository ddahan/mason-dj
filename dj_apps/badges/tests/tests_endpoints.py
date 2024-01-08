import datetime

from django.contrib.auth import get_user_model

import pytest

from core.utils.testing_utils import api_url
from profiles.factories import UserFactory

from ..factories import BadgeFactory
from ..models.badge import Badge

User = get_user_model()

##########################################################################################
# SHARED BADGE FIXTURES
##########################################################################################


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def badges(db, user) -> list[Badge]:
    return [
        BadgeFactory(owner=user, is_active=True),
        BadgeFactory(),
    ]


##########################################################################################
# LIST BADGES
##########################################################################################

list_badges_url = api_url("list_badges")


# def test_list_badges_unauthenticated(badges, client):
#     response = client.get(list_badges_url)
#     assert response.status_code == 401


def test_list_badges_empty(auth_headers, client):
    response = client.get(list_badges_url, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0


def test_list_badges_ok(badges, auth_headers, client):
    response = client.get(list_badges_url, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2


##########################################################################################
# RETRIEVE BADGE
##########################################################################################


# def test_retrieve_badge_unauthenticated(badges, client):
#     response = client.get(api_url("retrieve_badge", identifier="some_identifier"))
#     assert response.status_code == 401


def test_retrieve_unexisting_badge(badges, auth_headers, client):
    url = api_url("retrieve_badge", identifier="wrong_identifier")
    response = client.get(url, headers=auth_headers)
    assert response.status_code == 404


def test_retrieve_badge_ok(badges, auth_headers, client):
    existing_identifier = badges[0].identifier
    url = api_url("retrieve_badge", identifier=existing_identifier)
    response = client.get(url, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["identifier"] == existing_identifier


##########################################################################################
# CREATE BADGE
##########################################################################################


def test_create_badge_ok(badges, user, auth_headers, client):
    nb_badges = Badge.objects.count()
    response = client.post(
        api_url("create_badge"),
        data={"owner_id": user.id, "is_active": True},
        headers=auth_headers,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert Badge.objects.count() == nb_badges + 1


def test_create_badge_ko_missing_data(badges, auth_headers, client):
    response = client.post(
        api_url("create_badge"),
        data={"is_active": True},
        headers=auth_headers,
        content_type="application/json",
    )
    assert response.status_code == 400


##########################################################################################
# UPDATE BADGE
##########################################################################################


def test_update_badge_ok(badges, auth_headers, client):
    badge = badges[0]
    assert badge.is_active is True
    some_date = datetime.datetime(2025, 1, 1, 12, 30, 0, 0, tzinfo=datetime.timezone.utc)
    response = client.put(
        api_url("update_badge", identifier=badge.identifier),
        data={
            "owner_id": UserFactory().id,
            "is_active": False,
            "expiration": some_date,
        },
        headers=auth_headers,
        content_type="application/json",
    )

    assert response.status_code == 200
    badge.refresh_from_db()
    assert badge.is_active is False
    assert badge.expiration == some_date


def test_update_badge_ko_missing_data(badges, auth_headers, client):
    response = client.put(
        api_url("update_badge", identifier=badges[0].identifier),
        data={
            "is_active": False,
        },
        headers=auth_headers,
        content_type="application/json",
    )
    assert response.status_code == 400


##########################################################################################
# UPDATE BADGE ACTIVITY
##########################################################################################


def test_update_badge_activity(db, badges, client, auth_headers):
    badge = badges[0]
    old_badge_activity = Badge.objects.get(identifier=badge.identifier).is_active
    response = client.patch(
        api_url("update_badge_activity", identifier=badge.identifier),
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert Badge.objects.get(identifier=badge.identifier).is_active != old_badge_activity


##########################################################################################
# DESTROY BADGE
##########################################################################################


def test_destroy_badge(db, badges, client, auth_headers):
    badge = badges[0]
    Badge.objects.get(identifier=badge.identifier)
    response = client.delete(
        api_url("destroy_badge", identifier=badge.identifier), headers=auth_headers
    )
    assert response.status_code == 200
    with pytest.raises(Badge.DoesNotExist):
        Badge.objects.get(identifier=badge.identifier)
