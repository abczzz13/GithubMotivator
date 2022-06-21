import pytest
from motivator.models import Payment


@pytest.mark.django_db
def test_payment_model_valid(goal):
    """
    GIVEN a Django application configured for testing
    WHEN valid data is used as input to the Payment Model
    THEN check that the data is correctly saved into the DB
    """
    payment = Payment.objects.create(
        mollie_id="tr_7xS7vsKBy4",
        amount_eur=10,
        checkout_url="https://www.mollie.com/checkout/select-issuer/ideal/QdCtWBhJAD",
        goal=goal,
    )

    payment.full_clean()
    payment.save()

    query_set = Payment.objects.filter(mollie_id="tr_7xS7vsKBy4")

    assert len(query_set) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payment_status, payment_char",
    [
        ("open", "o"),
        ("canceled", "c"),
        ("pending", "u"),
        ("authorized", "a"),
        ("expired", "e"),
        ("failed", "f"),
        ("paid", "p"),
    ],
)
def test_process_payment_status(payment_status, payment_char):
    """
    GIVEN a Django application configured for testing
    WHEN a payment status is used in the Payment.process_payment_status()
    THEN the correct abbreviation is returned
    """
    assert Payment.process_payment_status(payment_status) == payment_char


@pytest.mark.django_db
def test_save_mollie_payment_into_db(goal):
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
    payment = Payment.save_mollie_payment_into_db(payment, goal)

    assert payment.mollie_id == "tr_QdCtWBhJAD"
    assert payment.amount_eur == 10
    assert payment.checkout_url == "https://www.mollie.com/checkout/select-issuer/ideal/QdCtWBhJAD"
    assert payment.payment_status == "o"
