"""Fixtures for Pytest"""
from typing import Any

import pytest
from django.conf import settings
from django.utils import timezone
from mixer.backend.django import mixer
from mollie.api.error import IdentifierError
from mollie.api.resources.base import ResourceBase
from mollie.api.resources.payment_refunds import PaymentRefunds
from mollie.api.resources.payments import Payments

from motivator.models import Goal
from motivator.payments import MolliePaymentProvider
from users.models import User, UserMotivator


class MockPaymentProvider:
    def patched_create(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Patched function to mimic the external Mollie API call"""
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
        payment["amount"]["value"] = payload["amount"]["value"]
        payment["description"] = payload["description"]
        payment["metadata"] = payload["metadata"]
        payment["redirectUrl"] = payload["redirectUrl"]
        payment["webhookUrl"] = payload["webhookUrl"]
        return payment

    def patched_get(self, id: str) -> dict[str, Any]:
        """Patched function to mimic the external Mollie API call"""
        payment = {
            "resource": "payment",
            "id": "tr_QdCtWBhJAD",
            "mode": "test",
            "createdAt": "2022-06-14T13:51:24+00:00",
            "amount": {"value": "10.00", "currency": "EUR"},
            "description": "Test #123",
            "method": "ideal",
            "metadata": {"order_id": "12345"},
            "status": "failed",
            "isCancelable": False,
            "expiresAt": "2022-06-14T14:06:24+00:00",
            "profileId": settings.MOLLIE_PROFILE_ID,
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
        if id != payment["id"]:
            raise IdentifierError("Payment could not be found")
        return payment

    def patched_refund(self, payload: dict[str, Any]) -> dict[str, Any]:
        refund = {
            "resource": "refund",
            "id": "re_4qqhO89gsT",
            "amount": {"currency": "EUR", "value": "5.95"},
            "status": "pending",
            "createdAt": "2018-03-14T17:09:02.0Z",
            "description": "Order #33",
            "metadata": {"bookkeeping_id": 12345},
            "paymentId": "tr_QdCtWBhJAD",
            "_links": {
                "self": {
                    "href": "https://api.mollie.com/v2/payments/tr_WDqYK6vllg/refunds/re_4qqhO89gsT",
                    "type": "application/hal+json",
                },
                "payment": {
                    "href": "https://api.mollie.com/v2/payments/tr_WDqYK6vllg",
                    "type": "application/hal+json",
                },
                "documentation": {
                    "href": "https://docs.mollie.com/reference/v2/refunds-api/create-payment-refund",
                    "type": "text/html",
                },
            },
        }
        refund["amount"]["value"] = payload["amount"]["value"]
        refund["description"] = payload["description"]
        refund["metadata"] = payload["metadata"]
        return refund

    def patched_on(self, payment: dict[str, Any]) -> str:
        return self.with_parent_id(payment["id"])


@pytest.fixture()
def patched_create(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ResourceBase, "create", MockPaymentProvider.patched_create)


@pytest.fixture()
def patched_get(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Payments, "get", MockPaymentProvider.patched_get)


@pytest.fixture()
def patched_on(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(PaymentRefunds, "on", MockPaymentProvider.patched_on)


@pytest.fixture()
def patched_refund(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ResourceBase, "create", MockPaymentProvider.patched_refund)


@pytest.fixture()
def user(db):
    motivator = mixer.blend(UserMotivator, github_username="abczzz13")
    test_user = mixer.blend(User, username="Test User")
    motivator.user = test_user
    motivator.save()
    test_user.save()
    return motivator


@pytest.fixture()
def goal(user):
    start_date = timezone.now() + timezone.timedelta(minutes=1)
    end_date = timezone.now() + timezone.timedelta(days=1)
    amount = 10
    motivator_goal = mixer.blend(Goal, start_date=start_date, end_date=end_date, amount=amount)
    motivator_goal.user = user.user
    return motivator_goal


@pytest.fixture()
def payment(monkeypatch: pytest.MonkeyPatch, goal):
    monkeypatch.setattr(ResourceBase, "create", MockPaymentProvider.patched_create)
    client = MolliePaymentProvider()
    payment = client.create_payment(goal)
    return payment


@pytest.fixture()
def registered_user(client, db):
    user = {
        "username": "Test_User",
        "email": "test@test.com",
        "password1": "PasswordofTestUser",
        "password2": "PasswordofTestUser",
        "github_username": "abczzz13",
    }

    client.post("/register/", user)

    return user


@pytest.fixture()
def authenticated_user(client, registered_user):

    client.login(
        username=registered_user["username"],
        password=registered_user["password1"],
    )

    return registered_user
