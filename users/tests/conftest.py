from mixer.backend.django import mixer
from users.models import User, UserMotivator
import pytest


@pytest.fixture()
def user(db):
    motivator = mixer.blend(UserMotivator)
    test_user = mixer.blend(User, username='Test User')
    motivator.user = test_user
    return motivator
