"""End-to-End Tests for testing the profile functionality"""
import pytest
from django.contrib.auth import get_user


def test_profile_authenticated(client, authenticated_user):
    """
    GIVEN a Django application configured for testing
    WHEN a GET request is made by an authenticated user to go to '/profile/'
    THEN check that the appropriate response is generated
    """
    response = client.get("/profile/")

    logged_in_user = get_user(client)

    assert logged_in_user.is_authenticated
    assert response.status_code == 200


@pytest.mark.parametrize(
    "username, email, github_username, status_code",
    [
        ("Test_User", "test@test.com", "testhub", 302),
        ("Test_User1", "test@test.com", "testhub", 302),
        ("Test_User", "test1@test.com", "testhub", 302),
        ("Test_User", "test@test.com", "testhub1", 302),
        ("", "test@test.com", "testhub", 200),
        ("Test_User", "", "testhub", 200),
        ("Test_User", "test@test.com", "", 200),
        ("Test_User", "geen_email", "testhub", 200),
    ],
)
def test_profile_authenticated_parameterized(
    username, email, github_username, status_code, client, authenticated_user
):
    """
    GIVEN a Django application configured for testing
    WHEN a POST request is made by an authenticated user to change
    parameterized profile settings
    THEN check that the appropriate response status_code is generated
    """
    data = {
        "username": username,
        "email": email,
        "github_username": github_username,
    }

    response = client.post("/profile/", data)

    assert response.status_code == status_code


@pytest.mark.django_db
def test_profile_unauthenticated(client):
    """
    GIVEN a Django application configured for testing
    WHEN a GET request is made by an unauthenticated user to go to '/profile/'
    THEN check that the appropriate response is generated
    """
    response = client.get("/profile/")

    logged_in_user = get_user(client)

    assert not logged_in_user.is_authenticated
    assert response.status_code == 302
