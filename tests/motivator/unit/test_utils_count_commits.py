from datetime import datetime

from django.utils import timezone
from motivator.models import Goal
from motivator.utils_motivator import count_commits


def test_utils_count_commits_valid(goal: Goal):
    """
    GIVEN a Django application configured for testing
    WHEN the commits of an active Github repo is counted
    THEN the count of this repo is more than 0
    """
    # This test currently only works if the commits on this project is active enough
    goal.github_username = "abczzz13"
    goal.repo = "GithubMotivator"

    goal.start_date = timezone.now() - timezone.timedelta(days=100)
    goal.end_date = timezone.now()

    assert count_commits(goal) > 0


def test_utils_count_commits_invalid_date(goal: Goal):
    """
    GIVEN a Django application configured for testing
    WHEN the commits are counted before the repo was active
    THEN no commits are counted
    """
    # This test currently only works if the commits on this project is active enough
    goal.github_username = "abczzz13"
    goal.repo = "GithubMotivator"
    goal.start_date = timezone.make_aware(datetime(year=2021, month=1, day=1))
    goal.end_date = timezone.make_aware(datetime(year=2021, month=1, day=31))

    assert count_commits(goal) == 0
