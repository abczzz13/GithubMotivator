"""Unit Tests for testing the Motivator Models"""
import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from mixer.backend.django import mixer
from motivator.models import Goal
from users.models import User


@pytest.mark.django_db
def test_goal_model_valid():
    """
    GIVEN a Django application configured for testing
    WHEN valid data is used as input to the Goal Model
    THEN check that the data is correctly saved into the DB
    """
    user = mixer.blend(User)

    goal = Goal.objects.create(
        github_username="test",
        repo="testrepo1",
        commit_goal=10,
        amount=10,
        start_date=timezone.now(),
        end_date=timezone.now() + timezone.timedelta(days=7),
        user=user,
    )

    goal.full_clean()
    goal.save()

    query_set = Goal.objects.filter(repo="testrepo1")

    assert len(query_set) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "repo, commit_goal, amount, start_date, end_date, value_error",
    [
        (
            "",
            10,
            10,
            timezone.now(),
            timezone.now() + timezone.timedelta(days=7),
            "field cannot be blank",
        ),
        (
            "testrepo3",
            10,
            "",
            timezone.now(),
            timezone.now() + timezone.timedelta(days=7),
            "value must be a decimal number",
        ),
        (
            "testrepo4",
            10,
            10,
            "",
            timezone.now() + timezone.timedelta(days=7),
            "value has an invalid format",
        ),
        (
            "testrepo5",
            10,
            10,
            timezone.now(),
            "",
            "value has an invalid format",
        ),
        (
            "testrepo6",
            0,
            10,
            timezone.now(),
            timezone.now() + timezone.timedelta(days=7),
            "value is greater than or equal",
        ),
        (
            "testrepo7",
            10,
            0,
            timezone.now(),
            timezone.now() + timezone.timedelta(days=7),
            "value is greater than or equal",
        ),
        (
            "testrepo8",
            10,
            10,
            timezone.now() - timezone.timedelta(days=7),
            timezone.now() + timezone.timedelta(days=7),
            "value is greater than or equal",
        ),
        (
            "testrepo9",
            10,
            10,
            timezone.now() - timezone.timedelta(days=7),
            timezone.now() - timezone.timedelta(days=1),
            "value is greater than or equal",
        ),
        (
            "testrepo10",
            10,
            10,
            timezone.now(),
            timezone.now() - timezone.timedelta(days=1),
            "value is greater than or equal",
        ),
    ],
)
def test_goal_model_validation_error(
    repo, commit_goal, amount, start_date, end_date, value_error
):
    """
    GIVEN a Django application configured for testing
    WHEN invalid parameterized data is used as input to the Goal Model
    THEN check that the correct ValidationErrors are raised
    """
    with pytest.raises(ValidationError) as err:
        user = mixer.blend(User)

        goal = Goal(
            github_username="test",
            repo=repo,
            commit_goal=commit_goal,
            amount=amount,
            start_date=start_date,
            end_date=end_date,
            user=user,
        )

        goal.full_clean()  # realistic to call this method to test the model?
        goal.save()

    assert value_error in str(err.value)
