"""Unit Tests for testing the forms functionality"""
import pytest
from django.utils import timezone
from motivator.forms import GoalForm


@pytest.mark.parametrize(
    "repo, commit_goal, amount, start_date, end_date, assertion",
    [
        (
            "testrepo",
            10,
            10,
            timezone.now(),
            timezone.now() + timezone.timedelta(days=7),
            True,
        ),
        (
            "",
            10,
            10,
            timezone.now(),
            timezone.now() + timezone.timedelta(days=7),
            False,
        ),
        (
            "testrepo",
            "",
            10,
            timezone.now(),
            timezone.now() + timezone.timedelta(days=7),
            False,
        ),
        (
            "testrepo",
            10,
            "",
            timezone.now(),
            timezone.now() + timezone.timedelta(days=7),
            False,
        ),
        (
            "testrepo",
            10,
            10,
            "",
            timezone.now() + timezone.timedelta(days=7),
            False,
        ),
        ("testrepo", 10, 10, timezone.now(), "", False),
        (
            "testrepo",
            0,
            10,
            timezone.now(),
            timezone.now() + timezone.timedelta(days=7),
            False,
        ),
        (
            "testrepo",
            10,
            0,
            timezone.now(),
            timezone.now() + timezone.timedelta(days=7),
            False,
        ),
        (
            "testrepo",
            10,
            10,
            timezone.now() - timezone.timedelta(days=7),
            timezone.now() + timezone.timedelta(days=7),
            False,
        ),
        (
            "testrepo",
            10,
            10,
            timezone.now() - timezone.timedelta(days=7),
            timezone.now() - timezone.timedelta(days=1),
            False,
        ),
        (
            "testrepo",
            10,
            10,
            timezone.now(),
            timezone.now() - timezone.timedelta(days=1),
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

    form = GoalForm(data)

    assert form.is_valid() == assertion
