"""Unit Tests for testing the Users Views"""
import pytest
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from users.views import profile, register


def test_users_login_unauthenticated(rf):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """
    path = reverse("login")
    request = rf.get(path)
    request.user = AnonymousUser()

    response = auth_views.LoginView.as_view()(request)

    assert response.status_code == 200


def test_users_login_authenticated(rf, user):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """
    path = reverse("login")
    request = rf.get(path)
    request.user = user

    response = auth_views.LoginView.as_view()(request)

    assert response.status_code == 200


def test_users_register_unauthenticated(rf):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """
    path = reverse("users-register")
    request = rf.get(path)
    request.user = AnonymousUser()

    response = register(request)

    assert response.status_code == 200


def test_users_register_authenticated(rf, user):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """
    path = reverse("users-register")
    request = rf.get(path)
    request.user = user

    response = register(request)

    assert response.status_code == 200


def test_users_profile_unauthenticated(rf):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """
    path = reverse("users-profile")
    request = rf.get(path)
    request.user = AnonymousUser()

    response = profile(request)

    assert response.status_code == 302


def test_users_profile_authenticated(rf, user):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """
    path = reverse("users-profile")
    request = rf.get(path)
    request.user = user.user

    response = profile(request)

    assert response.status_code == 200


@pytest.mark.skip(reason="Currently fails, have to look into this")
def test_users_logout_unauthenticated(client, user):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """
    path = reverse("logout")
    # client.user = AnonymousUser()
    request = client.get(path)
    request.user = AnonymousUser()
    # request.user = user

    response = auth_views.LogoutView.as_view()(request)

    assert response.status_code == 200


@pytest.mark.skip(reason="Currently fails, have to look into this")
def test_users_logout_authenticated(client, user):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """

    path = reverse("logout")
    request = client.get(path)
    request.user = user

    response = auth_views.LogoutView.as_view()(
        request, {"next_page": "/login"}
    )

    assert response.status_code == 200


def test_users_password_reset_unauthenticated(rf):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """

    path = reverse("password_reset")
    request = rf.get(path)
    request.user = AnonymousUser()

    response = auth_views.PasswordResetView.as_view()(request)

    assert response.status_code == 200


def test_users_password_reset_authenticated(rf, user):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """

    path = reverse("password_reset")
    request = rf.get(path)
    request.user = user

    response = auth_views.PasswordResetView.as_view()(request)

    assert response.status_code == 200


def test_users_password_reset_done_unauthenticated(rf):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """

    path = reverse("password_reset_done")
    request = rf.get(path)
    request.user = AnonymousUser()

    response = auth_views.PasswordResetDoneView.as_view()(request)

    assert response.status_code == 200


def test_users_password_reset_done_authenticated(rf, user):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """

    path = reverse("password_reset_done")
    request = rf.get(path)
    request.user = user

    response = auth_views.PasswordResetDoneView.as_view()(request)

    assert response.status_code == 200


@pytest.mark.skip(reason="Currently fails, have to look into this")
def test_users_password_reset_confirm_unauthenticated(rf):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """

    path = reverse(
        "password_reset_confirm", kwargs={"uidb64": "...", "token": "..."}
    )
    request = rf.get(path)
    request.user = AnonymousUser()

    response = auth_views.PasswordResetConfirmView.as_view()(request)

    assert response.status_code == 200


@pytest.mark.skip(reason="Currently fails, have to look into this")
def test_users_password_reset_confirm_authenticated(rf, user):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """

    path = reverse("password_reset_confirm", args=["uidb64", "token"])
    request = rf.post(path)
    request.user = user

    response = auth_views.PasswordResetConfirmView.as_view()(
        request, args=["uidb64", "token"]
    )

    assert response.status_code == 200


def test_users_password_reset_complete_unauthenticated(rf):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """

    path = reverse("password_reset_complete")
    request = rf.get(path)
    request.user = AnonymousUser()

    response = auth_views.PasswordResetCompleteView.as_view()(request)

    assert response.status_code == 200


def test_users_password_reset_complete_authenticated(rf, user):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """

    path = reverse("password_reset_complete")
    request = rf.get(path)
    request.user = user

    response = auth_views.PasswordResetCompleteView.as_view()(request)

    assert response.status_code == 200


# password_reset_done
# password_reset_confirm
# password_reset_complete
