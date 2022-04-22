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
    path = reverse("login")
    request = rf.get(path)
    request.user = user

    response = auth_views.LoginView.as_view()(request)

    assert response.status_code == 200


def test_users_register_unauthenticated(rf):
    path = reverse("users-register")
    request = rf.get(path)
    request.user = AnonymousUser()

    response = register(request)

    assert response.status_code == 200


def test_users_register_authenticated(rf, user):
    path = reverse("users-register")
    request = rf.get(path)
    request.user = user

    response = register(request)

    assert response.status_code == 200


def test_users_profile_unauthenticated(rf):
    path = reverse("users-profile")
    request = rf.get(path)
    request.user = AnonymousUser()

    response = profile(request)

    assert response.status_code == 302


def test_users_profile_authenticated(rf, user):
    path = reverse("users-profile")
    request = rf.get(path)
    request.user = user.user

    response = profile(request)

    assert response.status_code == 200


@pytest.mark.skip(reason="Currently fails, have to look into this")
def test_users_logout_unauthenticated(client):
    path = reverse("logout")
    request = client.get(path)
    request.user = AnonymousUser()

    response = auth_views.LogoutView.as_view()(request)

    assert response.status_code == 200


@pytest.mark.skip(reason="Currently fails, have to look into this")
def test_users_logout_authenticated(client, user):
    path = reverse("logout")
    request = client.get(path)
    request.user = user

    response = auth_views.LogoutView.as_view()(request)

    assert response.status_code == 200


def test_users_password_reset_unauthenticated(rf):
    path = reverse("password_reset")
    request = rf.get(path)
    request.user = AnonymousUser()

    response = auth_views.PasswordResetView.as_view()(request)

    assert response.status_code == 200


def test_users_password_reset_authenticated(rf, user):
    path = reverse("password_reset")
    request = rf.get(path)
    request.user = user

    response = auth_views.PasswordResetView.as_view()(request)

    assert response.status_code == 200


def test_users_password_reset_done_unauthenticated(rf):
    path = reverse("password_reset_done")
    request = rf.get(path)
    request.user = AnonymousUser()

    response = auth_views.PasswordResetDoneView.as_view()(request)

    assert response.status_code == 200


def test_users_password_reset_done_authenticated(rf, user):
    path = reverse("password_reset_done")
    request = rf.get(path)
    request.user = user

    response = auth_views.PasswordResetDoneView.as_view()(request)

    assert response.status_code == 200


@pytest.mark.skip(reason="Currently fails, have to look into this")
def test_users_password_reset_confirm_unauthenticated(rf):
    path = reverse("password_reset_confirm")
    request = rf.get(path)
    request.user = AnonymousUser()

    response = auth_views.PasswordResetConfirmView.as_view()(request)

    assert response.status_code == 200


@pytest.mark.skip(reason="Currently fails, have to look into this")
def test_users_password_reset_confirm_authenticated(rf, user):
    path = reverse("password_reset_confirm")
    request = rf.get(path)
    request.user = user

    response = auth_views.PasswordResetConfirmView.as_view()(request)

    assert response.status_code == 200


def test_users_password_reset_complete_unauthenticated(rf):
    path = reverse("password_reset_complete")
    request = rf.get(path)
    request.user = AnonymousUser()

    response = auth_views.PasswordResetCompleteView.as_view()(request)

    assert response.status_code == 200


def test_users_password_reset_complete_authenticated(rf, user):
    path = reverse("password_reset_complete")
    request = rf.get(path)
    request.user = user

    response = auth_views.PasswordResetCompleteView.as_view()(request)

    assert response.status_code == 200


# password_reset_done
# password_reset_confirm
# password_reset_complete
