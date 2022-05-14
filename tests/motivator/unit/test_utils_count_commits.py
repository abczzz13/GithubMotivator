from datetime import datetime, timedelta

import pytest
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
    goal.start_date = datetime.now() - timedelta(days=21)
    goal.end_date = datetime.now()

    count = count_commits(goal)

    assert count > 0
