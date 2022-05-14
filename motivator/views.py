from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from users.models import UserMotivator

from .forms import GoalForm
from .models import Goal
from .utils_motivator import count_commits


def index(request):
    """View for the homepage of the website"""
    return render(request, "motivator/index.html", {"title": "Home"})


class ListGoal(LoginRequiredMixin, ListView):
    """Overview of all the Goals"""

    model = Goal
    context_object_name = "goals"

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["commit_goals"] = []
        for goal in context["goals"]:
            commit_goal = {"goal": goal, "count": count_commits(goal)}
            context["commit_goals"].append(commit_goal)
        return context


class DetailGoal(LoginRequiredMixin, DetailView):
    """View where the user can see the details of a specified Goal"""

    model = Goal
    context_object_name = "goal"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["commit_count"] = count_commits(context["goal"])
        return context


class CreateGoal(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """View where the user can create a new Goal"""

    model = Goal
    form_class = GoalForm
    success_message = "Your goal has been set"

    def get_form_kwargs(self):
        """Get the extra parameters for the form to validate the repo url"""
        self.github_username = (
            UserMotivator.objects.filter(user=self.request.user)
            .first()
            .github_username
        )
        kwargs = super(CreateGoal, self).get_form_kwargs()
        kwargs["github_username"] = self.github_username
        return kwargs

    def get_success_url(self):
        return reverse("goal-list")

    def form_valid(self, form):
        """Adds the extra fields to save in the Model"""
        form.instance.user = self.request.user
        form.instance.github_username = self.github_username
        return super(CreateGoal, self).form_valid(form)
