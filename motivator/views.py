from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from users.models import UserMotivator
from .forms import GoalForm
from .models import Goal, Payment


def index(request):
    return render(request, 'motivator/index.html', {'title': 'Home'})


@login_required
def goals(request):
    if request.method == 'POST':
        goal_form = GoalForm(request.POST, instance=request.user)

        if goal_form.is_valid():
            goal = goal_form.save(commit=False)
            goal.save()
            messages.success(
                request, 'Your goal has been set')

            return HttpResponseRedirect('/')

    else:

        # Check database if any goals are open for the current user and show them?
        # Goals.objects.filter(...).first()
        # filter on current user and status in progress

        goal_form = GoalForm(instance=request.user)

        context = {
            'goal_form': goal_form,
        }

    return render(request, 'motivator/goals.html', context)


class ListGoal(LoginRequiredMixin, ListView):
    model = Goal
    context_object_name = 'goals'

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class DetailGoal(LoginRequiredMixin, DetailView):
    model = Goal
    context_object_name = 'goal'


class CreateGoal(LoginRequiredMixin, CreateView):
    model = Goal
    fields = ['repo', 'commit_goal', 'amount', 'start_date', 'end_date']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.github_username = UserMotivator.objects.filter(
            user=self.request.user).first().github_username
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('goal-list')
