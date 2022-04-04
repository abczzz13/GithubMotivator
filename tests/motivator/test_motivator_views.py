'''Testing the view functions of the Motivator App'''
from django.urls import reverse
from motivator.views import index, CreateGoal, ListGoal, DetailGoal
import pytest


def test_motivator_index(rf):
    '''
    GIVEN a Django application configured for testing
    WHEN a GET request is made to 'motivator-index' view function
    THEN check that the response is valid
    '''
    path = reverse('motivator-index')
    request = rf.get(path)

    response = index(request)

    assert response.status_code == 200


def test_motivator_goals(rf, goal):
    '''
    GIVEN a Django application configured for testing
    WHEN a GET request is made to 'goal-list' view function
    THEN check that the response is valid
    '''
    path = reverse('goal-list')
    request = rf.get(path)
    request.user = goal.user

    response = ListGoal.as_view()(request)

    assert response.status_code == 200


# No reverse match
def test_motivator_goals_detail(rf, goal):
    '''
    GIVEN a Django application configured for testing
    WHEN a GET request is made to 'goal-detail' view function
    THEN check that the response is valid
    '''
    path = reverse('goal-detail', goal.id)
    request = rf.get(path)
    request.user = goal.user

    response = DetailGoal.as_view()(request, pk=goal.id)

    assert response.status_code == 200


def test_motivator_goals_create(rf, user):
    '''
    GIVEN a Django application configured for testing
    WHEN a GET request is made to 'goal-create' view function
    THEN check that the response is valid
    '''
    path = reverse('goal-create')
    request = rf.get(path)
    request.user = user.user

    response = CreateGoal.as_view()(request)

    assert response.status_code == 200
