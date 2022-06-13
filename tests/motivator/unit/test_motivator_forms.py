"""Unit Tests for testing the forms functionality"""
import pytest
from django.utils import timezone
from motivator.forms import GoalForm

now = timezone.now()
last_week = timezone.now() - timezone.timedelta(days=7)
next_week = timezone.now() + timezone.timedelta(days=7)
last_day = timezone.now() - timezone.timedelta(days=1)


@pytest.mark.parametrize(
    "repo, commit_goal, amount, start_date, end_date, assertion",
    [
        (
            "GithubMotivator",
            10,
            10,
            now,
            next_week,
            True,
        ),
        (
            "",
            10,
            10,
            now,
            next_week,
            False,
        ),
        (
            "testrepo",
            "",
            10,
            now,
            next_week,
            False,
        ),
        (
            "testrepo",
            10,
            "",
            now,
            next_week,
            False,
        ),
        (
            "testrepo",
            10,
            10,
            "",
            next_week,
            False,
        ),
        ("testrepo", 10, 10, now, "", False),
        (
            "testrepo",
            0,
            10,
            now,
            next_week,
            False,
        ),
        (
            "testrepo",
            10,
            0,
            now,
            next_week,
            False,
        ),
        (
            "testrepo",
            10,
            10,
            last_week,
            next_week,
            False,
        ),
        (
            "testrepo",
            10,
            10,
            last_week,
            last_day,
            False,
        ),
        (
            "testrepo",
            10,
            10,
            now,
            last_day,
            False,
        ),
    ],
)
def test_goal_form(repo, commit_goal, amount, start_date, end_date, assertion):
    """
    GIVEN a Django application configured for testing
    WHEN parameterized data is used as input to the Goal Form
    THEN check that the data is correctly validated
    """
    data = {
        "repo": repo,
        "commit_goal": commit_goal,
        "amount": amount,
        "start_date": start_date,
        "end_date": end_date,
    }
    form = GoalForm("abczzz13", data)
    assert form.is_valid() == assertion
