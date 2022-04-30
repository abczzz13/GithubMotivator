from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone

from .models import Goal
from .utils import get_response_from_url


class GoalForm(ModelForm):
    class Meta:
        model = Goal
        fields = ["repo", "commit_goal", "amount", "start_date", "end_date"]

    def __init__(self, github_username, *args, **kwargs):
        self.github_username = github_username
        super().__init__(*args, **kwargs)

    def validate_dates(self, start_date, end_date):
        if start_date and end_date:
            if end_date < start_date:
                raise ValidationError(
                    {
                        "start_date": "Start date must be before end date",
                        "end_date": "Or... change this field",
                    }
                )
            elif start_date < timezone.now() - timezone.timedelta(minutes=30):
                raise ValidationError(
                    {
                        "start_date": "Start date cannot be in the past",
                    }
                )
            elif end_date < timezone.now() - timezone.timedelta(minutes=30):
                raise ValidationError(
                    {
                        "end_date": "End date cannot be in the past",
                    }
                )

    def validate_repo(self, github_username, repo):
        url = f"https://github.com/{github_username}/{repo}"
        if "message" in get_response_from_url(url):
            raise ValidationError(
                {"repo": "This Github repository could not be found."}
            )

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        repo = cleaned_data.get("repo")

        self.validate_dates(start_date, end_date)
        self.validate_repo(self.github_username, repo)

        return cleaned_data
