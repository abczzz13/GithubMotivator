from django.db import models
from django.utils import timezone


class Goals(models.Model):
    # repositories =  # List in Mongo, one-to-many table in sql...
    commit_goal = models.PositiveIntegerField()
    status = models.CharField(max_length=1)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    # payment =  # object in Mongo, one-to-one/many table in sql...


class Payments(models.Model):
    mollie_id = models.CharField(max_length=255)
    amount_eur = models.CharField(max_length=255)
    checkout_url = models.URLField()
    status = models.CharField(max_length=1)
    datetime = models.DateTimeField()
