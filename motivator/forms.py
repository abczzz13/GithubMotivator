from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone

from .models import Goal


class GoalForm(ModelForm):
    class Meta:
        model = Goal
        fields = ["repo", "commit_goal", "amount", "start_date", "end_date"]

    # Need something as form validation
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

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

        return cleaned_data
