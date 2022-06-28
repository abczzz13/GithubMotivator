from datetime import datetime

from django.conf import settings
from django.utils import timezone

from .models import Goal
from .utils import get_response_from_url


def parse_github_datetime(event_datetime: str) -> datetime:
    """Parse the Github UTC time to Europe/Amsterdam Timezone object"""
    date_time = event_datetime[:-1].replace("T", " ")
    github_utc_time = timezone.make_aware(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S"))
    return github_utc_time + timezone.timedelta(hours=2)


def count_commits(goal: Goal) -> int:
    """Counts the amount commits for the provided Goal that have been made"""
    count = 0
    base_url = "https://api.github.com/repos/"
    url = f"{base_url}{goal.github_username}/{goal.repo}/events"
    headers = {"Time-Zone": settings.TIME_ZONE}

    data = get_response_from_url(url, headers)

    if "message" in data:
        # Think about specific error message for this situation?
        print(data["message"], url)
        return "Error!"

    for event in data.json():
        print(event["created_at"])
        event_datetime = parse_github_datetime(event["created_at"])
        if goal.start_date < event_datetime < goal.end_date:
            if "commits" in event["payload"]:
                for commit in event["payload"]["commits"]:
                    count += 1
        else:
            # Github API orders the data from recent to older
            return count

    return count
