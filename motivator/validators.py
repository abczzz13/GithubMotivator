"""Custom validators to validate fields in the Models"""
from django.core.exceptions import ValidationError
from django.utils import timezone


def date_validator_min(value):
    """
    Validator to validate the submitted date cannot be in past

    Inserted a 30 minutes margin to prevent any user unfriendly errors
    """
    if value < (timezone.now() - timezone.timedelta(minutes=30)):
        raise ValidationError("Date cannot be in the past")
    else:
        return value
