from abc import ABC, abstractmethod
from typing import Any

from django.conf import settings
from mollie.api.client import Client
from mollie.api.error import RequestError, RequestSetupError

from .models import Goal, Payment, Refund

"""
Errors:
- mollie.api.error.RequestError -> no connection
- mollie.api.error.RequestSetupError -> api key not set
"""
Json = dict[str, Any]


class PaymentProvider(ABC):
    @abstractmethod
    def create_payment(self, goal: Goal) -> Payment:
        """Create payment, save it to DB and return the Payment object"""

    @abstractmethod
    def get_payment(self, id: str) -> Json:
        """Get payment info and return as json"""

    @abstractmethod
    def create_refund(self, id: str) -> Refund:
        """Create refund and return the refund as json"""

    @abstractmethod
    def save_payment(self, payment: Json, goal: Goal) -> Payment:
        """Save payment into the DB"""

    @abstractmethod
    def save_refund(self, payment: Payment, goal: Goal) -> Refund:
        """Save refund into the DB"""

    @abstractmethod
    def get_or_create_payment_link(self, goal: Goal) -> str:
        """Returns payment link if valid, else creates new payment"""


class MolliePaymentProvider(PaymentProvider):
    client = Client()

    def __init__(self) -> None:
        self.client.set_api_key(settings.MOLLIE_API_KEY)

    def __str__(self) -> str:
        return "MolliePaymentProvider"

    def create_payment(self, goal: Goal) -> Payment:
        """Create Mollie payment"""
        payload = {
            "amount": {
                "currency": "EUR",
                "value": self.amount_to_str(goal.amount),
            },
            "description": f"Goal #{goal.pk}",
            "redirectUrl": "http://localhost:8000/goals/",
            "webhookUrl": f"{settings.MOLLIE_PUBLIC_URL}/mollie/",
            "metadata": {
                "goal_id": goal.pk,
                "user_id": goal.user.id,
            },
        }
        mollie_payment = self.client.payments.create(payload)
        payment = self.save_payment(mollie_payment, goal)
        return payment

    def get_payment(self, id: str) -> Json:
        """Get payment info from Mollie"""
        # catching errors?
        payment = self.client.payments.get(id)
        return payment

    def create_refund(self, payment: Payment, goal: Goal) -> Refund:
        """Create Mollie refund"""
        mollie_payment = self.get_payment(payment.payment_id)
        print(payment)
        print(payment.amount_eur)
        payload = {
            "amount": {
                "currency": "EUR",
                "value": self.amount_to_str(payment.amount_eur),
            },
            "description": f"Refund for goal {goal.pk} with payment {payment.payment_id}",
            "metadata": {
                "goal_id": goal.pk,
                "user_id": goal.user.id,
                "payment_id": payment.payment_id,
            },
        }
        mollie_refund = self.client.payment_refunds.on(mollie_payment).create(payload)
        refund = self.save_refund(mollie_refund, payment, goal)
        # verify if refund was created successfully?
        # what to with saving refunds in the DB?
        return refund

    def get_or_create_payment_link(self, goal: Goal) -> str:
        """Returns payment link if valid, else creates new payment"""
        payment = Payment.objects.filter(goal=goal, payment_status="o").first()
        if not payment:
            payment = self.create_payment(goal)
        return payment.checkout_url

    def save_payment(self, mollie_payment: Json, goal: Goal) -> Payment:
        """Save the mollie payment into the DB"""
        payment = Payment(
            payment_id=mollie_payment["id"],
            amount_eur=float(mollie_payment["amount"]["value"]),
            checkout_url=mollie_payment["_links"]["checkout"]["href"],
            payment_status="o",
            goal=goal,
        )
        payment.save()
        return payment

    def save_refund(self, mollie_refund: Json, payment: Payment, goal: Goal) -> Refund:
        """Save the refund into the DB"""
        refund = Refund(
            refund_id=mollie_refund["id"],
            amount_eur=float(mollie_refund["amount"]["value"]),
            refund_status="o",
            payment=payment,
            goal=goal,
        )
        refund.save()
        return refund

    @staticmethod
    def amount_to_str(amount: int) -> str:
        """Convert amount to a str for creating a Mollie payment"""
        return str(f"{amount:.2f}")
