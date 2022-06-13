from datetime import datetime

from django.utils import timezone
from motivator.models import Goal
from motivator.utils_motivator import count_commits


def test_utils_count_commits_valid(goal: Goal):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN

    >>> This test currently only works if the commits on this project is active enough
    """
    goal.github_username = "abczzz13"
    goal.repo = "GithubMotivator"

    goal.start_date = timezone.now() - timezone.timedelta(days=100)
    goal.end_date = timezone.now()

    count = count_commits(goal)

    assert count > 0


def test_utils_count_commits_invalid_date(goal: Goal):
    """
    GIVEN a Django application configured for testing
    WHEN
    THEN

    >>> This test currently only works if the commits on this project is active enough
    """
    goal.github_username = "abczzz13"
    goal.repo = "GithubMotivator"
    goal.start_date = timezone.make_aware(datetime(year=2021, month=1, day=1))
    goal.end_date = timezone.make_aware(datetime(year=2021, month=1, day=31))

    count = count_commits(goal)

    assert count == 0
