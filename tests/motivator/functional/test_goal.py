"""End-to-End Tests for testing the goal overview functionality"""
import pytest
from django.contrib.auth import get_user


def test_goal_authenticated(client, authenticated_user):
    """
    GIVEN a Django application configured for testing
    WHEN a GET request is made by an authenticated user to go to '/goals/'
    THEN check that the appropriate response is generated
    """
    response = client.get("/goals/")

    logged_in_user = get_user(client)

    assert logged_in_user.is_authenticated
    assert response.status_code == 200


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_goal_unauthenticated(client):
    """
    GIVEN a Django application configured for testing
    WHEN a GET request is made by an unauthenticated user to go to '/profile/'
    THEN check that the appropriate response is generated
    """
    response = client.get("/goals/")

    logged_in_user = get_user(client)

    assert not logged_in_user.is_authenticated
    assert response.status_code == 302
