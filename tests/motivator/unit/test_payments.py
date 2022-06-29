import pytest
from motivator.models import Goal, Payment, Refund
from motivator.payments import PaymentProvider


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_payment_valid(payment_client: PaymentProvider, patched_create, goal: Goal):
    """
    GIVEN a Django application configured for testing
    WHEN a payment is created from a valid goal
    THEN a valid payment is returned and saved in the DB
    """
    payment = payment_client.create_payment(goal)

    assert payment.amount_eur == goal.amount
    assert payment.goal.id == goal.pk
    assert payment.goal.user.id == goal.user.id
    assert payment.payment_status == "o"
    assert payment.checkout_url == "https://www.mollie.com/checkout/select-issuer/ideal/QdCtWBhJAD"
    assert len(Payment.objects.filter(id=goal.pk)) == 1


def test_create_payment_invalid():
    """
    GIVEN
    WHEN
    THEN
    """
    pass


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_payment_info(payment_client: PaymentProvider, patched_get, payment: Payment):
    """
    GIVEN a Django application configured for testing
    WHEN an existing payment is retrieved from the PaymentProvider
    THEN the valid payment data is returned
    """
    mollie_payment = payment_client.get_payment(payment.payment_id)

    assert mollie_payment["id"] == "tr_QdCtWBhJAD"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_refund_valid(
    payment_client: PaymentProvider,
    payment: Payment,
    goal: Goal,
    patched_refund,
    patched_get,
    patched_on,
):
    """
    GIVEN a Django application configured for testing
    WHEN a refund is created based on existing goal and payment
    THEN a valid refund is created
    """
    refund = payment_client.create_refund(payment, goal)

    assert refund.amount_eur == 10
    assert refund.refund_status == "o"
    assert refund.payment == payment
    assert refund.goal == goal
    assert len(Refund.objects.filter(refund_id=refund.refund_id)) == 1


def test_create_refund_invalid():
    """
    GIVEN
    WHEN
    THEN
    """
    pass


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_or_create_payment_existing_payment(
    payment_client: PaymentProvider, patched_create, goal: Goal, payment: Payment
):
    """
    GIVEN a Django application configured for testing
    WHEN an existing payment link is requested with the get_or_create function
    THEN the payment_link is returned from this payment
    """
    payment_link = payment_client.get_or_create_payment_link(goal)

    assert payment_link == "https://www.mollie.com/checkout/select-issuer/ideal/QdCtWBhJAD"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_get_or_create_payment_new_payment(
    payment_client: PaymentProvider, patched_create, goal: Goal
):
    """
    GIVEN a Django application configured for testing
    WHEN a new payment link is requested with the get_or_create function
    THEN a new payment is created and the payment_link is returned
    """
    payment_link = payment_client.get_or_create_payment_link(goal)

    assert payment_link == "https://www.mollie.com/checkout/select-issuer/ideal/QdCtWBhJAD"


def test_get_or_create_payment_invalid():
    """
    GIVEN
    WHEN
    THEN
    """
    pass


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_save_payment_valid(payment_client: PaymentProvider, goal: Goal):
    """
    GIVEN a Django application configured for testing
    WHEN a payment is created with Mollie API
    THEN the Mollie payment is correctly saved into the DB
    """
    payment = {
        "resource": "payment",
        "id": "tr_QdCtWBhJAD",
        "mode": "test",
        "createdAt": "2022-06-14T13:51:24+00:00",
        "amount": {"value": "10.00", "currency": "EUR"},
        "description": "Test #123",
        "method": "ideal",
        "metadata": {"order_id": "12345"},
        "status": "open",
        "isCancelable": False,
        "expiresAt": "2022-06-14T14:06:24+00:00",
        "profileId": "pfl_3uCm3wEJgB",
        "sequenceType": "oneoff",
        "redirectUrl": "https://webshop.example.org/order/12345/",
        "webhookUrl": "https://64eb-86-83-204-47.eu.ngrok.io",
        "_links": {
            "self": {
                "href": "https://api.mollie.com/v2/payments/tr_QdCtWBhJAD",
                "type": "application/hal+json",
            },
            "checkout": {
                "href": "https://www.mollie.com/checkout/select-issuer/ideal/QdCtWBhJAD",
                "type": "text/html",
            },
            "dashboard": {
                "href": "https://www.mollie.com/dashboard/org_1251741/payments/tr_QdCtWBhJAD",
                "type": "text/html",
            },
            "documentation": {
                "href": "https://docs.mollie.com/reference/v2/payments-api/create-payment",
                "type": "text/html",
            },
        },
    }
    payment = payment_client.save_payment(payment, goal)

    assert payment.payment_id == "tr_QdCtWBhJAD"
    assert payment.amount_eur == 10
    assert payment.checkout_url == "https://www.mollie.com/checkout/select-issuer/ideal/QdCtWBhJAD"
    assert payment.payment_status == "o"


def test_save_payment_invalid():
    """
    GIVEN
    WHEN
    THEN
    """
    pass
