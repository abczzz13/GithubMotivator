import pytest
from motivator.utils import get_response_from_url


def test_get_response_from_url_valid_data():
    """
    GIVEN a Django application configured for testing
    WHEN an external call is made to the Github API with a valid repo
    THEN check that there is no error message
    """
    url = "https://api.github.com/repos/abczzz13/GithubMotivator/events"
    response = get_response_from_url(url)

    assert "message" not in response


@pytest.mark.parametrize(
    "url, result",
    [
        (
            "https://api.github.com/repos/abczzz13/GithubMotivator/eventsz",
            "HTTPError",
        ),
        ("https://test.tdejong.io/", "RequestException"),
        ("", "RequestException"),
        (
            "https://api.github.com/repos/abczzzx13/GithubMotivator/events",
            "HTTPError",
        ),
        (
            "https://api.github.com/repos/abczzz13/GithubMotivatorz/events",
            "HTTPError",
        ),
    ],
)
def test_get_response_from_url_invalid_data(url: str, result: str):
    """
    GIVEN a Django application configured for testing
    WHEN an external call is made to the Github API with a invalid repo
    THEN check that there is an error message
    """
    response = get_response_from_url(url)
    assert response["message"] == result


@pytest.mark.parametrize(
    "url, result",
    [
        (
            "https://github.com/abczzz13",
            200,
        ),
        (
            "https://github.com/abczzz13/GithubMotivator",
            200,
        ),
    ],
)
def test_utils_get_response_from_url_valid_status_code(url: str, result: int):
    """
    GIVEN a Django application configured for testing
    WHEN an external call is made to the Github API with a valid url
    THEN a status code of 200 is returned
    """
    response = get_response_from_url(url)
    assert response.status_code == result


@pytest.mark.parametrize(
    "url, result",
    [
        (
            "https://github.com/abczzz13/GithubMotivatorz",
            {"message": "HTTPError"},
        ),
    ],
)
def test_utils_get_response_from_url_invalid_status_code(url: str, result: dict[str, str]):
    """
    GIVEN a Django application configured for testing
    WHEN an external call is made to the Github API with a invalid repo
    THEN the appropriate error is raised
    """
    response = get_response_from_url(url)
    assert response == result
