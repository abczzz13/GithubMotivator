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
        payment_id="tr_7xS7vsKBy4",
        amount_eur=10,
        checkout_url="https://www.mollie.com/checkout/select-issuer/ideal/QdCtWBhJAD",
        goal=goal,
    )

    payment.full_clean()
    payment.save()

    query_set = Payment.objects.filter(payment_id="tr_7xS7vsKBy4")

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
