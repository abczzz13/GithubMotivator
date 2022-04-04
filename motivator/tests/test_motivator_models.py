from mixer.backend.django import mixer
import pytest


@pytest.mark.django_db
class TestMotivatorModels:

    def test_goals(self):
        # Mixer libary
        # user = mixer.blend('users.UserMotivator', ...)
        goal = mixer.blend('motivator.Goal')
        pass
