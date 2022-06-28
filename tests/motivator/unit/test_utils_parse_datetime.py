import pytest
from django.utils import timezone
from motivator.utils_motivator import parse_github_datetime


@pytest.mark.parametrize(
    "event_datetime, result",
    [
        ("2022-04-25T12:09:04Z", timezone.datetime(2022, 4, 25, 14, 9, 4)),
        ("2022-03-25T09:58:46Z", timezone.datetime(2022, 3, 25, 11, 58, 46)),
    ],
)
def test_goal_model_validation_error(event_datetime, result):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    ! please note the time correction from Github time +2 hours
    """
    output = parse_github_datetime(event_datetime)

    assert output == timezone.make_aware(result)
