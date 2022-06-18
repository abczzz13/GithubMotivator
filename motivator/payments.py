from typing import Any

from django.conf import settings
from mollie.api.client import Client
from mollie.api.error import RequestError

from .models import Goal, Payment

"""
Errors:
- mollie.api.error.RequestError
"""


class MolliePaymentProvider:
    client = Client()

    def __init__(self) -> None:
        self.client.set_api_key(settings.MOLLIE_API_KEY)

    def create_payment(self, goal: Goal):
        """Create Mollie payment"""
        # catching errors?
        payload = {
            "amount": {
                "currency": "EUR",
                "value": self.amount_to_str(goal.amount),
            },
            "description": f"Goal #{goal.pk} ",
            "redirectUrl": "http://localhost:8000/goals/",
            "webhookUrl": f"{settings.MOLLIE_PUBLIC_URL}/mollie/",
            "metadata": {
                "goal_id": goal.pk,
                "user_id": goal.user.id,
            },
        }
        payment = self.client.payments.create(payload)
        return payment

    def get_payment_info(self, id: str):
        """Get payment info from Mollie"""
        # catching errors?
        payment = self.client.payments.get(id)
        return payment

    def create_refund(self, id: str) -> str:
        """Create Mollie refund"""
        payment = self.get_payment_info(id)

        payload = {
            "amount": {
                "currency": "EUR",
                "value": self.amount_to_str(payment["amount"]["value"]),
            },
            "description": f"Refund for {payment['description']}",
            "metadata": payment["metadata"],
        }
        refund = self.client.payment_refunds.on(payment).create(payload)
        # verify if refund was created successfully?
        return refund["id"]

    def save_payment_into_db(self, mollie_payment: dict[str, Any], goal: Goal) -> Payment:
        """Save the mollie payment into the DB"""
        payment = Payment(
            mollie_id=mollie_payment["id"],
            amount_eur=mollie_payment["amount"]["value"],
            checkout_url=mollie_payment["_links"]["checkout"]["href"],
            payment_status="o",
            goal=goal,
        )
        payment.save()
        return payment

    @staticmethod
    def amount_to_str(amount: int) -> str:
        """Convert amount to a str for creating a Mollie payment"""
        return str(f"{amount:.2f}")


json = {
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

"""
{
    "resource": "payment",
    "id": "tr_7xS7vsKBy4",
    "mode": "test",
    "createdAt": "2022-06-16T07:36:29+00:00",
    "amount": {"value": "1000.00", "currency": "EUR"},
    "description": "Goal #48",
    "method": "ideal",
    "metadata": {"goal_id": 48, "user_id": 1},
    "status": "paid",
    "paidAt": "2022-06-16T07:36:35+00:00",
    "amountRefunded": {"value": "0.00", "currency": "EUR"},
    "amountRemaining": {"value": "1025.00", "currency": "EUR"},
    "locale": "en_NL",
    "countryCode": "NL",
    "profileId": "pfl_3uCm3wEJgB",
    "sequenceType": "oneoff",
    "redirectUrl": "http://localhost:8000/goals/",
    "webhookUrl": "https://bddb-86-83-204-47.eu.ngrok.io/mollie/",
    "settlementAmount": {"value": "1000.00", "currency": "EUR"},
    "details": {
        "consumerName": "T. TEST",
        "consumerAccount": "NL12RABO0995764688",
        "consumerBic": "TRIONL2U",
    },
    "_links": {
        "self": {
            "href": "https://api.mollie.com/v2/payments/tr_7xS7vsKBy4",
            "type": "application/hal+json",
        },
        "dashboard": {
            "href": "https://www.mollie.com/dashboard/org_1251741/payments/tr_7xS7vsKBy4",
            "type": "text/html",
        },
        "changePaymentState": {
            "href": "https://www.mollie.com/checkout/test-mode?method=ideal&token=4.k2tq0w",
            "type": "text/html",
        },
        "documentation": {
            "href": "https://docs.mollie.com/reference/v2/payments-api/get-payment",
            "type": "text/html",
        },
    },
}
"""
