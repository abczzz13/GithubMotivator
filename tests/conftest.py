"""Fixtures for Pytest"""
import pytest
from django.utils import timezone
from mixer.backend.django import mixer

from motivator.models import Goal
from users.models import User, UserMotivator


@pytest.fixture()
def user(db):
    motivator = mixer.blend(UserMotivator, github_username="abczzz13")
    test_user = mixer.blend(User, username="Test User")
    motivator.user = test_user
    motivator.save()
    test_user.save()
    return motivator


@pytest.fixture()
def goal(user):
    start_date = timezone.now() + timezone.timedelta(minutes=1)
    end_date = timezone.now() + timezone.timedelta(days=1)
    motivator_goal = mixer.blend(
        Goal, start_date=start_date, end_date=end_date
    )
    motivator_goal.user = user.user
    return motivator_goal


@pytest.fixture()
def registered_user(client, db):
    user = {
        "username": "Test_User",
        "email": "test@test.com",
        "password1": "PasswordofTestUser",
        "password2": "PasswordofTestUser",
        "github_username": "abczzz13",
    }

    client.post("/register/", user)

    return user


@pytest.fixture()
def authenticated_user(client, registered_user):

    client.login(
        username=registered_user["username"],
        password=registered_user["password1"],
    )

    return registered_user
