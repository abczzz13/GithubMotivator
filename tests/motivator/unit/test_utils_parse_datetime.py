from datetime import datetime

import pytest
from motivator.utils_motivator import parse_github_datetime


@pytest.mark.parametrize(
    "event_datetime, result",
    [
        ("2022-04-25T12:09:04Z", datetime(2022, 4, 25, 12, 9, 4)),
        ("2022-03-25T09:58:46Z", datetime(2022, 3, 25, 9, 58, 46)),
    ],
)
def test_goal_model_validation_error(event_datetime, result):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN
    """

    assert parse_github_datetime(event_datetime) == result
