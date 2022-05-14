"""Utility functions for the the GithubMotivator App"""
import requests
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import (
    HTTPError,
    RequestException,
    Timeout,
    TooManyRedirects,
)


def get_response_from_url(url: str) -> dict[str, str] or requests.Response:
    """Making a request to an url to get the response"""
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)

    with requests.Session() as http:
        http.mount("https://", adapter)
        http.mount("http://", adapter)

        try:
            response = http.get(url)
            response.raise_for_status()
        except Timeout:
            print("Retry?")
            return {"message": "Timeout"}
        except HTTPError:
            return {"message": "HTTPError"}
        except TooManyRedirects:
            return {"message": "TooManyRedirects"}
        except RequestException:
            return {"message": "RequestException"}

    return response
