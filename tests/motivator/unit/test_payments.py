import pytest
from motivator.models import Goal, Payment
from motivator.payments import MolliePaymentProvider


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_payment_valid(patched_create, goal: Goal):
    """
    GIVEN
    WHEN
    THEN
    """
    client = MolliePaymentProvider()
    payment = client.create_payment(goal)

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


@pytest.mark.django_db
def test_get_payment_info(patched_get):
    """
    GIVEN
    WHEN
    THEN
    """
    client = MolliePaymentProvider()
    payment = client.get_payment("tr_QdCtWBhJAD")

    assert payment["id"] == "tr_QdCtWBhJAD"


@pytest.mark.django_db
def test_create_refund_valid(patched_refund, patched_get, patched_on):
    """
    GIVEN
    WHEN
    THEN
    """
    client = MolliePaymentProvider()
    refund = client.create_refund("tr_QdCtWBhJAD")
    # what to with saving refunds in the DB?
    assert float(refund["amount"]["value"]) == 10
    assert refund["description"] == "Refund for Test #123"
    assert refund["metadata"] == {"order_id": "12345"}


def test_create_refund_invalid():
    """
    GIVEN
    WHEN
    THEN
    """
    pass


@pytest.mark.django_db
def test_get_or_create_payment_valid(patched_create, goal):
    """
    GIVEN
    WHEN
    THEN
    """
    client = MolliePaymentProvider()
    payment_link = client.get_or_create_payment_link(goal)

    assert payment_link == "https://www.mollie.com/checkout/select-issuer/ideal/QdCtWBhJAD"


def test_get_or_create_payment_invalid():
    """
    GIVEN
    WHEN
    THEN
    """
    pass


def test_save_payment_valid():
    """
    GIVEN
    WHEN
    THEN
    """
    pass


def test_save_payment_invalid():
    """
    GIVEN
    WHEN
    THEN
    """
    pass
