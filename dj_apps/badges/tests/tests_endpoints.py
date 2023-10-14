from django.contrib.auth import get_user_model

import pytest

from core.utils.testing_utils import api_url

from ..models.badge import Badge
from .factories import BadgeFactory

User = get_user_model()

##########################################################################################
# SHARED BADGE FIXTURES
##########################################################################################


@pytest.fixture
def badges(db) -> list[Badge]:
    return [
        BadgeFactory(sid="12345", is_active=True),
        BadgeFactory(),
    ]


##########################################################################################
# LIST BADGES
##########################################################################################

list_badges_url = api_url("list_badges")


def test_list_badges_unauthenticated(badges, client):
    response = client.get(list_badges_url)
    assert response.status_code == 401


def test_list_badges_empty(auth_headers, client):
    response = client.get(list_badges_url, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_list_badges_ok(badges, auth_headers, client):
    response = client.get(list_badges_url, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


##########################################################################################
# RETRIEVE BADGE
##########################################################################################


def test_retrieve_badge_unauthenticated(badges, client):
    response = client.get(api_url("retrieve_badge", sid="some_sid"))
    assert response.status_code == 401


def test_retrieve_unexisting_badge(badges, auth_headers, client):
    url = api_url("retrieve_badge", sid="wrong_sid")
    response = client.get(url, headers=auth_headers)
    assert response.status_code == 404


def test_retrieve_badge_ok(badges, auth_headers, client):
    existing_sid = badges[0].sid
    url = api_url("retrieve_badge", sid=existing_sid)
    response = client.get(url, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["sid"] == existing_sid


##########################################################################################
# CREATE BADGE
##########################################################################################


@pytest.mark.parametrize(
    "payload, expected",
    [
        [{}, 200],  # no data
        [{"sid": "LnM915Qf3DdavBeCjZUSwk"}, 200],  # correct sid
        [{"is_active": False}, 200],  # correct is_active
        [{"sid": "12345"}, 400],  # already existing badge
    ],
)
def test_create_badge_ok(badges, db, client, auth_headers, payload, expected):
    nb_badges = Badge.objects.count()
    response = client.post(
        api_url("create_badge"),
        data=payload,
        headers=auth_headers,
        content_type="application/json",
    )
    assert response.status_code == expected
    assert Badge.objects.count() == (nb_badges + 1 if expected == 200 else nb_badges)


##########################################################################################
# UPDATE BADGE
##########################################################################################

# TODO: if we want to test the return values, it seems a little complex with parametrize
# Find a trick OR remove parametrize


@pytest.mark.parametrize(
    "payload, expected_status_code",
    [
        [{}, 200],  # no data, no change
        [{"sid": "123"}, 200],  # sid won't be changed
        [{"is_active": False}, 200],  # is_active will be changed
    ],
)
def test_update_badge(badges, db, client, auth_headers, payload, expected_status_code):
    response = client.put(
        api_url("update_badge", sid="12345"),
        data=payload,
        headers=auth_headers,
        content_type="application/json",
    )

    assert response.status_code == expected_status_code


##########################################################################################
# UPDATE BADGE ACTIVITY
##########################################################################################


# def test_update_badge_activity(db):
#     ...

##########################################################################################
# DESTROY BADGE
##########################################################################################

# def test_destroy_badge(db):
#     ...
