"""End-to-End Tests for testing the logout functionality"""
import pytest
from django.contrib.auth import get_user


def test_logout_valid(client, authenticated_user):
    """
    GIVEN a Django application configured for testing
    WHEN a POST request is made to logout an authenticated user on /logout/
    THEN check that the appropriate response is generated
    """

    response = client.post("/logout/")

    logged_in_user = get_user(client)

    assert not logged_in_user.is_authenticated
    assert response.status_code == 200


def test_logout_invalid(client, registered_user):
    """
    GIVEN a Django application configured for testing
    WHEN a POST request is made to logout an unauthenticated user on /logout/
    THEN check that the appropriate response is generated
    """

    response = client.post("/logout/")

    logged_in_user = get_user(client)

    assert not logged_in_user.is_authenticated
    assert response.status_code == 200
