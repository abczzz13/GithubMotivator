"""Unit Tests for testing the Users Models"""
import pytest
from mixer.backend.django import mixer
from users.models import User, UserMotivator


@pytest.mark.django_db
def test_users():
    """
    GIVEN a Django application configured for testing
    WHEN valid data is used as input to the Goal Model
    THEN check that the data is correctly saved into the DB
    """
    # Mixer libary
    # user = mixer.blend('users.UserMotivator', ...)
    pass


@pytest.mark.django_db
def test_create_user():
    """
    GIVEN a Django application configured for testing
    WHEN valid data is used as input to the extended User Motivator Model
    THEN check that the data is correctly saved into the DB
    """
    user = mixer.blend(User, username="Test User", email="test@test.com")
    motivator = mixer.blend(UserMotivator)
    motivator.user = user
    motivator.user.save()

    new_user = User.objects.get(username="Test User")

    assert new_user.email == "test@test.com"
