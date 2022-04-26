"""Unit Tests for testing the Users urls"""
from django.urls import resolve, reverse


def test_register():
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """
    path = reverse("users-register")

    assert resolve(path).view_name == "users-register"


def test_login():
    path = reverse("login")

    assert resolve(path).view_name == "login"


def test_logout():
    path = reverse("logout")

    assert resolve(path).view_name == "logout"


def test_profile():
    path = reverse("users-profile")

    assert resolve(path).view_name == "users-profile"


def test_password_reset():
    path = reverse("password_reset")

    assert resolve(path).view_name == "password_reset"


def test_password_reset_done():
    path = reverse("password_reset_done")

    assert resolve(path).view_name == "password_reset_done"


def test_password_reset_confirm():
    path = reverse(
        "password_reset_confirm", kwargs={"uidb64": 1, "token": "abcdefgh"}
    )

    assert resolve(path).view_name == "password_reset_confirm"


def test_password_reset_complete():
    path = reverse("password_reset_complete")

    assert resolve(path).view_name == "password_reset_complete"
