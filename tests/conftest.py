'''Fixtures for Pytest'''
from mixer.backend.django import mixer
from motivator.models import Goal
from users.models import User, UserMotivator
import pytest


@pytest.fixture()
def user(db):
    motivator = mixer.blend(UserMotivator)
    test_user = mixer.blend(User, username='Test User')
    motivator.user = test_user
    return motivator


@pytest.fixture()
def goal(user):
    motivator_goal = mixer.blend(Goal)
    motivator_goal.user = user.user
    return motivator_goal
