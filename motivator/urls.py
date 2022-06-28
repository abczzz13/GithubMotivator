"""Motivator App URL Configuration"""
from django.urls import path

from .views import (
    CreateGoal,
    DetailGoal,
    ListGoal,
    get_payment_link,
    index,
    mollie_webhook,
)

urlpatterns = [
    path("", index, name="motivator-index"),
    path("goals/", ListGoal.as_view(), name="goal-list"),
    path("goals/new/", CreateGoal.as_view(), name="goal-create"),
    path("goals/<pk>/", DetailGoal.as_view(), name="goal-detail"),
    path("goals/<pk>/payment/", get_payment_link, name="get-payment-link"),
    path("mollie/", mollie_webhook, name="mollie-webhook"),
]
