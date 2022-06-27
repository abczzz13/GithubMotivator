from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from users.models import User

from motivator.validators import date_validator_min

STATUS_OPEN = "o"
STATUS_CANCELED = "c"
STATUS_PENDING = "u"
STATUS_AUTHORIZED = "a"
STATUS_EXPIRED = "e"
STATUS_FAILED = "f"
STATUS_PAID = "p"
STATUS_CHOICES = [
    (STATUS_OPEN, "open"),
    (STATUS_CANCELED, "canceled"),
    (STATUS_PENDING, "pending"),
    (STATUS_AUTHORIZED, "authorized"),
    (STATUS_EXPIRED, "expired"),
    (STATUS_FAILED, "failed"),
    (STATUS_PAID, "paid"),
]


class Goal(models.Model):
    GOAL_STATUS_IN_PROGRESS = "i"
    GOAL_STATUS_SUCCESS = "s"
    GOAL_STATUS_FAILED = "f"
    GOAL_STATUS_CHOICES = [
        (GOAL_STATUS_IN_PROGRESS, "in progress"),
        (GOAL_STATUS_SUCCESS, "succesfull"),
        (GOAL_STATUS_FAILED, "failed"),
    ]
    github_username = models.CharField(max_length=255)
    repo = models.CharField(max_length=255, validators=[MinLengthValidator(3)])
    commit_goal = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    amount = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    status = models.CharField(max_length=1, choices=GOAL_STATUS_CHOICES, default="i")
    start_date = models.DateTimeField(default=timezone.now, validators=[date_validator_min])
    end_date = models.DateTimeField(validators=[date_validator_min])
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def _validate_start_end_dates(self):
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                raise ValidationError("End date cannot be before start date.")
            elif self.start_date < timezone.now() - timezone.timedelta(minutes=30):
                raise ValidationError("Start date cannot be in the past")
            elif self.end_date < timezone.now() - timezone.timedelta(minutes=30):
                raise ValidationError("End date cannot be in the past")

    def save(self, *args, **kwargs):
        self._validate_start_end_dates()
        return super().save(*args, **kwargs)


class Payment(models.Model):
    payment_id = models.CharField(max_length=255)
    amount_eur = models.DecimalField(max_digits=5, decimal_places=2)
    checkout_url = models.URLField()
    payment_status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
    )
    datetime = models.DateTimeField(default=timezone.now)
    goal = models.ForeignKey(Goal, on_delete=models.PROTECT, null=True, related_name="payment")

    @staticmethod
    def process_payment_status(status: str):
        for choice in STATUS_CHOICES:
            if choice[1] == status:
                return choice[0]

    def __str__(self) -> str:
        return f"Payment {self.payment_id}: EUR {self.amount_eur} on date: {self.datetime} for goal: {self.goal} with status: {self.payment_status}"


class Refund(models.Model):
    refund_id = models.CharField(max_length=255)
    amount_eur = models.DecimalField(max_digits=5, decimal_places=2)
    refund_status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
    )
    datetime = models.DateTimeField(default=timezone.now)
    goal = models.ForeignKey(Goal, on_delete=models.PROTECT, null=True, related_name="refund")
    payment = models.ForeignKey(
        Payment, on_delete=models.PROTECT, null=True, related_name="payment"
    )

    @staticmethod
    def process_payment_status(status: str):
        for choice in STATUS_CHOICES:
            if choice[1] == status:
                return choice[0]

    # def __str__(self) -> str:
    #     return f"Payment {self.mollie_id}: EUR {self.amount_eur} on date: {self.datetime} for goal: {self.goal} with status: {self.payment_status}"
