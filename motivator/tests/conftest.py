from mixer.backend.django import mixer
from users.models import User, UserMotivator
from motivator.models import Goal
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
