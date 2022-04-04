from mixer.backend.django import mixer
from users.models import UserMotivator, User
import pytest


@pytest.mark.django_db
class TestUsersModels:

    def test_users(self):
        # Mixer libary
        # user = mixer.blend('users.UserMotivator', ...)
        pass


@pytest.mark.django_db
def test_create_user():
    user = mixer.blend(User, username='Test User', email='test@test.com')
    motivator = mixer.blend(UserMotivator)
    motivator.user = user
    motivator.user.save()

    new_user = User.objects.get(username='Test User')

    assert new_user.email == 'test@test.com'
