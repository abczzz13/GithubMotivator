from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from users.models import UserMotivator

from .forms import GoalForm
from .models import Goal


def index(request):
    return render(request, "motivator/index.html", {"title": "Home"})


class ListGoal(LoginRequiredMixin, ListView):
    model = Goal
    context_object_name = "goals"

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class DetailGoal(LoginRequiredMixin, DetailView):
    model = Goal
    context_object_name = "goal"


class CreateGoal(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Goal
    form_class = GoalForm
    success_message = "Your goal has been set"

    def get_form_kwargs(self):
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
        form.instance.user = self.request.user
        form.instance.github_username = self.github_username
        return super(CreateGoal, self).form_valid(form)
