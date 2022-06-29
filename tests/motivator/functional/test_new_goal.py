"""End-to-End Tests for testing the create goal functionality"""
import pytest
from django.contrib.auth import get_user
from django.utils import timezone


def test_create_goal_authenticated(client, authenticated_user):
    """
    GIVEN a Django application configured for testing
    WHEN a GET request is made by an authenticated user to go to '/goals/new/'
    THEN check that the appropriate response is generated
    """
    response = client.get("/goals/new/")

    logged_in_user = get_user(client)

    assert logged_in_user.is_authenticated
    assert response.status_code == 200


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_create_goal_unauthenticated(client):
    """
    GIVEN a Django application configured for testing
    WHEN a GET request is made by an unauthenticated user to go
    to '/profile/new/'
    THEN check that the appropriate response is generated
    """
    response = client.get("/goals/new/")

    logged_in_user = get_user(client)

    assert not logged_in_user.is_authenticated
    assert response.status_code == 302


@pytest.mark.parametrize(
    "repo, commit_goal, amount, start_date, end_date, status_code",
    [
        (
            "GithubMotivator",
            10,
            10,
            timezone.now(),
            timezone.now() + timezone.timedelta(days=7),
            302,
        ),
        (
            "",
            10,
            10,
            timezone.now(),
            timezone.now() + timezone.timedelta(days=7),
            200,
        ),
        (
            "GithubMotivator",
            "",
            10,
            timezone.now(),
            timezone.now() + timezone.timedelta(days=7),
            200,
        ),
        (
            "GithubMotivator",
            10,
            "",
            timezone.now(),
            timezone.now() + timezone.timedelta(days=7),
            200,
        ),
        (
            "GithubMotivator",
            10,
            10,
            "",
            timezone.now() + timezone.timedelta(days=7),
            200,
        ),
        ("GithubMotivator", 10, 10, timezone.now(), "", 200),
        (
            "tGithubMotivator",
            0,
            10,
            timezone.now(),
            timezone.now() + timezone.timedelta(days=7),
            200,
        ),
        (
            "GithubMotivator",
            10,
            0,
            timezone.now(),
            timezone.now() + timezone.timedelta(days=7),
            200,
        ),
        (
            "GithubMotivator",
            10,
            10,
            timezone.now() - timezone.timedelta(days=7),
            timezone.now() + timezone.timedelta(days=7),
            200,
        ),
        (
            "GithubMotivator",
            10,
            10,
            timezone.now() - timezone.timedelta(days=7),
            timezone.now() - timezone.timedelta(days=1),
            200,
        ),
        (
            "GithubMotivator",
            10,
            10,
            timezone.now(),
            timezone.now() - timezone.timedelta(days=1),
            200,
        ),
    ],
)
def test_create_goal_authenticated_parameterized(
    repo,
    commit_goal,
    amount,
    start_date,
    end_date,
    status_code,
    client,
    authenticated_user,
):
    """
    GIVEN a Django application configured for testing
    WHEN a POST request is made by an authenticated user to create
    parameterized goals
    THEN check that the appropriate response status_code is generated
    """
    data = {
        "repo": repo,
        "commit_goal": commit_goal,
        "amount": amount,
        "start_date": start_date,
        "end_date": end_date,
    }

    response = client.post("/goals/new/", data)

    # database query
    # Goal.objects.all().count

    assert response.status_code == status_code
