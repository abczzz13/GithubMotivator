from typing import Any

import pytest
from django.conf import settings
from mollie.api.error import IdentifierError
from mollie.api.resources.base import ResourceBase
from mollie.api.resources.payment_refunds import PaymentRefunds
from mollie.api.resources.payments import Payments
from motivator.models import Goal, Payment
from motivator.payments import MolliePaymentProvider
from pytest import MonkeyPatch

# class MockPaymentProvider:
#     def patched_create(self, payload: dict[str, Any]) -> dict[str, Any]:
#         """Patched function to mimic the external Mollie API call"""
#         payment = {
#             "resource": "payment",
#             "id": "tr_QdCtWBhJAD",
#             "mode": "test",
#             "createdAt": "2022-06-14T13:51:24+00:00",
#             "amount": {"value": "10.00", "currency": "EUR"},
#             "description": "Test #123",
#             "method": "ideal",
#             "metadata": {"order_id": "12345"},
#             "status": "open",
#             "isCancelable": False,
#             "expiresAt": "2022-06-14T14:06:24+00:00",
#             "profileId": "pfl_3uCm3wEJgB",
#             "sequenceType": "oneoff",
#             "redirectUrl": "https://webshop.example.org/order/12345/",
#             "webhookUrl": "https://64eb-86-83-204-47.eu.ngrok.io",
#             "_links": {
#                 "self": {
#                     "href": "https://api.mollie.com/v2/payments/tr_QdCtWBhJAD",
#                     "type": "application/hal+json",
#                 },
#                 "checkout": {
#                     "href": "https://www.mollie.com/checkout/select-issuer/ideal/QdCtWBhJAD",
#                     "type": "text/html",
#                 },
#                 "dashboard": {
#                     "href": "https://www.mollie.com/dashboard/org_1251741/payments/tr_QdCtWBhJAD",
#                     "type": "text/html",
#                 },
#                 "documentation": {
#                     "href": "https://docs.mollie.com/reference/v2/payments-api/create-payment",
#                     "type": "text/html",
#                 },
#             },
#         }
#         payment["amount"]["value"] = payload["amount"]["value"]
#         payment["description"] = payload["description"]
#         payment["metadata"] = payload["metadata"]
#         payment["redirectUrl"] = payload["redirectUrl"]
#         payment["webhookUrl"] = payload["webhookUrl"]
#         return payment

#     def patched_get(self, id: str) -> dict[str, Any]:
#         """Patched function to mimic the external Mollie API call"""
#         payment = {
#             "resource": "payment",
#             "id": "tr_QdCtWBhJAD",
#             "mode": "test",
#             "createdAt": "2022-06-14T13:51:24+00:00",
#             "amount": {"value": "10.00", "currency": "EUR"},
#             "description": "Test #123",
#             "method": "ideal",
#             "metadata": {"order_id": "12345"},
#             "status": "failed",
#             "isCancelable": False,
#             "expiresAt": "2022-06-14T14:06:24+00:00",
#             "profileId": settings.MOLLIE_PROFILE_ID,
#             "sequenceType": "oneoff",
#             "redirectUrl": "https://webshop.example.org/order/12345/",
#             "webhookUrl": "https://64eb-86-83-204-47.eu.ngrok.io",
#             "_links": {
#                 "self": {
#                     "href": "https://api.mollie.com/v2/payments/tr_QdCtWBhJAD",
#                     "type": "application/hal+json",
#                 },
#                 "checkout": {
#                     "href": "https://www.mollie.com/checkout/select-issuer/ideal/QdCtWBhJAD",
#                     "type": "text/html",
#                 },
#                 "dashboard": {
#                     "href": "https://www.mollie.com/dashboard/org_1251741/payments/tr_QdCtWBhJAD",
#                     "type": "text/html",
#                 },
#                 "documentation": {
#                     "href": "https://docs.mollie.com/reference/v2/payments-api/create-payment",
#                     "type": "text/html",
#                 },
#             },
#         }
#         if id != payment["id"]:
#             raise IdentifierError("Payment could not be found")
#         return payment

#     def patched_refund(self, payload: dict[str, Any]) -> dict[str, Any]:
#         refund = {
#             "resource": "refund",
#             "id": "re_4qqhO89gsT",
#             "amount": {"currency": "EUR", "value": "5.95"},
#             "status": "pending",
#             "createdAt": "2018-03-14T17:09:02.0Z",
#             "description": "Order #33",
#             "metadata": {"bookkeeping_id": 12345},
#             "paymentId": "tr_QdCtWBhJAD",
#             "_links": {
#                 "self": {
#                     "href": "https://api.mollie.com/v2/payments/tr_WDqYK6vllg/refunds/re_4qqhO89gsT",
#                     "type": "application/hal+json",
#                 },
#                 "payment": {
#                     "href": "https://api.mollie.com/v2/payments/tr_WDqYK6vllg",
#                     "type": "application/hal+json",
#                 },
#                 "documentation": {
#                     "href": "https://docs.mollie.com/reference/v2/refunds-api/create-payment-refund",
#                     "type": "text/html",
#                 },
#             },
#         }
#         refund["amount"]["value"] = payload["amount"]["value"]
#         refund["description"] = payload["description"]
#         refund["metadata"] = payload["metadata"]
#         return refund

#     def patched_on(self, payment: dict[str, Any]) -> str:
#         return self.with_parent_id(payment["id"])


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_payment_valid(patched_create, goal: Goal):
    """
    GIVEN
    WHEN
    THEN
    """
    # monkeypatch to prevent external API call
    # monkeypatch.setattr(ResourceBase, "create", MockPaymentProvider.patched_create)

    client = MolliePaymentProvider()
    payment = client.create_payment(goal)

    assert payment.amount_eur == goal.amount
    assert payment.goal.id == goal.pk
    assert payment.goal.user.id == goal.user.id
    assert payment.payment_status == "o"
    assert payment.checkout_url == "https://www.mollie.com/checkout/select-issuer/ideal/QdCtWBhJAD"
    # assert float(payment["amount"]["value"]) == goal.amount
    # assert payment["description"] == f"Goal #{goal.pk}"
    # assert payment["metadata"]["goal_id"] == goal.pk
    # assert payment["metadata"]["user_id"] == goal.user.id
    # assert payment["redirectUrl"] == "http://localhost:8000/goals/"
    # assert payment["webhookUrl"] == f"{settings.MOLLIE_PUBLIC_URL}/mollie/"
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
    # monkeypatch.setattr(Payments, "get", MockPaymentProvider.patched_get)

    client = MolliePaymentProvider()
    payment = client.get_payment_info("tr_QdCtWBhJAD")

    assert payment["id"] == "tr_QdCtWBhJAD"


@pytest.mark.django_db
def test_create_refund_valid(patched_refund, patched_get, patched_on):
    """
    GIVEN
    WHEN
    THEN
    """
    # monkeypatch.setattr(ResourceBase, "create", MockPaymentProvider.patched_refund)
    # monkeypatch.setattr(Payments, "get", MockPaymentProvider.patched_get)
    # monkeypatch.setattr(PaymentRefunds, "on", MockPaymentProvider.patched_on)

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
    # monkeypatch.setattr(ResourceBase, "create", MockPaymentProvider.patched_create)

    client = MolliePaymentProvider()
    payment_link = client.get_or_create_payment(goal)

    assert payment_link == "https://www.mollie.com/checkout/select-issuer/ideal/QdCtWBhJAD"


def test_get_or_create_payment_invalid():
    """
    GIVEN
    WHEN
    THEN
    """
    pass
