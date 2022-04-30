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


# def validator_url_alive(value):
#     url = f"https://github.com/{self.github_username}/{self.repo}"
#     if "message" in get_response_from_url(url):
#         raise ValidationError(
#             {"repo": "This Github repository could not be found."}
#         )
#     else:
#         return value
