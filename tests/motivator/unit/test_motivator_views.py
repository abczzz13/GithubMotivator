"""Testing the view functions of the Motivator App"""
import pytest
from django.urls import reverse
from motivator.models import Payment
from motivator.views import (
    CreateGoal,
    DetailGoal,
    ListGoal,
    get_payment_link,
    index,
    payment_webhook,
)


def test_motivator_index(rf):
    """
    GIVEN a Django application configured for testing
    WHEN a GET request is made to 'motivator-index' view function
    THEN check that the response is valid
    """
    path = reverse("motivator-index")
    request = rf.get(path)

    response = index(request)

    assert response.status_code == 200


def test_motivator_goals(rf, goal):
    """
    GIVEN a Django application configured for testing
    WHEN a GET request is made to 'goal-list' view function
    THEN check that the response is valid
    """
    path = reverse("goal-list")
    request = rf.get(path)
    request.user = goal.user

    response = ListGoal.as_view()(request)

    assert response.status_code == 200


def test_motivator_goals_detail(rf, goal):
    """
    GIVEN a Django application configured for testing
    WHEN a GET request is made to 'goal-detail' view function
    THEN check that the response is valid
    """
    path = reverse("goal-detail", args=[goal.id])
    request = rf.get(path)
    request.user = goal.user

    response = DetailGoal.as_view()(request, pk=goal.id)

    assert response.status_code == 200


def test_motivator_goals_create(rf, user):
    """
    GIVEN a Django application configured for testing
    WHEN a GET request is made to 'goal-create' view function
    THEN check that the response is valid
    """
    path = reverse("goal-create")
    request = rf.get(path)
    request.user = user.user

    response = CreateGoal.as_view()(request)

    assert response.status_code == 200


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_motivator_get_payment_link(patched_create, rf, goal):
    """
    GIVEN a Django application configured for testing
    WHEN a get request is made to the payment of an existing goal
    THEN the client will de redirected to the checkout_url
    """
    path = reverse("get-payment-link", args=[goal.pk])
    request = rf.get(path)

    response = get_payment_link(request, pk=goal.pk)

    payment = Payment.objects.filter(goal=goal.pk).first()

    assert response.status_code == 302
    assert response.url == payment.checkout_url


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_motivator_get_payment_link_invalid(rf):
    """
    GIVEN a Django application configured for testing
    WHEN a get request is made to the payment of an non existing goal
    THEN the client will de redirected to goal overview page
    """
    goal_id = 99
    path = reverse("get-payment-link", args=[goal_id])
    request = rf.get(path)

    response = get_payment_link(request, pk=goal_id)

    assert response.status_code == 302
    assert response.url == "/goals/"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_motivator_webhook_valid(patched_get, rf, payment):
    """
    GIVEN a Django application configured for testing
    WHEN a get request is made to the webhook with appropriate data
    THEN the response will be 200, status update will be fetched and updated in the DB
    """
    path = reverse("payment-webhook")
    request = rf.post(path, data={"id": payment.payment_id})

    response = payment_webhook(request)

    updated_payment = Payment.objects.filter(payment_id=payment.payment_id).first()

    assert response.status_code == 200
    assert updated_payment.payment_status == "f"


@pytest.mark.parametrize(
    "data",
    [{}, {"id": "test007"}, {"else": "something"}],
)
@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_motivator_webhook_invalid(rf, data):
    """
    GIVEN a Django application configured for testing
    WHEN a get request is made to the webhook with invalid data
    THEN the response will be 400
    """
    path = reverse("payment-webhook")
    request = rf.post(path, data=data)

    response = payment_webhook(request)

    assert response.status_code == 400
