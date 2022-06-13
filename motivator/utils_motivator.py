from datetime import datetime

from django.utils import timezone

from .models import Goal
from .utils import get_response_from_url


def parse_github_datetime(event_datetime: str) -> datetime:
    """Parse the created_at field from github api into datetime object"""
    date_time = event_datetime[:-1].replace("T", " ")

    github_time = timezone.make_aware(
        datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    )
    # github_time_correction = timezone.timedelta(hours=2)
    corrected_github_time = github_time + timezone.timedelta(hours=2)
    return corrected_github_time


def count_commits(goal: Goal) -> int:
    """Counts the amount commits for the provided Goal that have been made"""
    count = 0
    base_url = "https://api.github.com/repos/"
    url = f"{base_url}{goal.github_username}/{goal.repo}/events"

    data = get_response_from_url(url)

    if "message" in data:
        # Think about specific error message for this situation?
        print(data["message"], url)
        return "Error!"

    for event in data.json():
        event_datetime = parse_github_datetime(event["created_at"])
        if goal.start_date < event_datetime < goal.end_date:
            if "commits" in event["payload"]:
                for commit in event["payload"]["commits"]:
                    count += 1
        else:
            # Github API seems to sort the data from most recent to older
            # Therefore, we can stop iterating once a data is outside the scope
            return count

    return count
