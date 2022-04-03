import uuid
from django.db import models
from django.utils import timezone
from users.models import User


class Goal(models.Model):
    GOAL_STATUS_IN_PROGRESS = 'i'
    GOAL_STATUS_SUCCESS = 's'
    GOAL_STATUS_FAILED = 'f'
    GOAL_STATUS_CHOICES = [
        (GOAL_STATUS_IN_PROGRESS, 'in progress'),
        (GOAL_STATUS_SUCCESS, 'succesfull'),
        (GOAL_STATUS_FAILED, 'failed')
    ]
    # https://github.com/doableware/djongo/issues/8
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    github_username = models.CharField(max_length=255)
    repo = models.CharField(max_length=255)
    commit_goal = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    status = models.CharField(
        max_length=1,
        choices=GOAL_STATUS_CHOICES,
        default='i')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Payment(models.Model):
    PAYMENT_STATUS_OPEN = 'o'
    PAYMENT_STATUS_CANCELED = 'c'
    PAYMENT_STATUS_PENDING = 'u'
    PAYMENT_STATUS_AUTHORIZED = 'a'
    PAYMENT_STATUS_EXPIRED = 'e'
    PAYMENT_STATUS_FAILED = 'f'
    PAYMENT_STATUS_PAID = 'p'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_OPEN, 'open'),
        (PAYMENT_STATUS_CANCELED, 'canceled'),
        (PAYMENT_STATUS_PENDING, 'pending'),
        (PAYMENT_STATUS_AUTHORIZED, 'authorized'),
        (PAYMENT_STATUS_EXPIRED, 'expired'),
        (PAYMENT_STATUS_FAILED, 'failed'),
        (PAYMENT_STATUS_PAID, 'paid')
    ]

    id = models.PositiveIntegerField(primary_key=True)
    mollie_id = models.CharField(max_length=255)
    amount_eur = models.CharField(max_length=255)
    checkout_url = models.URLField()
    payment_status = models.CharField(
        max_length=1,
        choices=PAYMENT_STATUS_CHOICES,
        default='o')
    datetime = models.DateTimeField()
    goal = models.ForeignKey(Goal, on_delete=models.PROTECT, null=True)
