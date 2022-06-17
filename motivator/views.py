from typing import Any

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView
from users.models import UserMotivator

<<<<<<< HEAD
from motivator.forms import GoalForm
from motivator.models import Goal, Payment
from motivator.utils_motivator import count_commits
=======
from .forms import GoalForm
from .models import Goal, Payment
from .payments import MolliePaymentProvider
from .utils_motivator import count_commits
>>>>>>> 870d39d (Added PaymentProvider class and refactored the views)


def index(request):
    """View for the homepage of the website"""
    return render(request, "motivator/index.html", {"title": "Home"})


@csrf_exempt
def mollie_webhook(request) -> HttpResponse:
    """Mollie Webhook for updating the payment status"""

    if "id" not in request.POST:
        return HttpResponse(status=400)
    id = request.POST["id"]

    payment_client = MolliePaymentProvider()
    payment = payment_client.get_payment_info(id)

    if payment["id"] == id and payment["profileId"] == settings.MOLLIE_PROFILE_ID:
        Payment.objects.filter(mollie_id=id).update(
            payment_status=Payment.process_payment_status(payment["status"])
        )

    return HttpResponse(status=200)
    # mollie payment status of failed causes the the mollie payment link to go invalid
    # Remake the payment link if payment has failed?


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

    def get_form_kwargs(self) -> dict[str, Any]:
        """Get the extra parameters for the form to validate the repo url"""
        self.github_username = (
            UserMotivator.objects.filter(user=self.request.user).first().github_username
        )
        kwargs = super(CreateGoal, self).get_form_kwargs()
        kwargs["github_username"] = self.github_username
        return kwargs

    def get_success_url(self) -> str:
        """Starts the Mollie payment process and redirects to the Mollie payment url"""
        return self.create_payment_url()

    def form_valid(self, form):
        """Adds the extra fields to save in the Model"""
        form.instance.user = self.request.user
        form.instance.github_username = self.github_username
        return super(CreateGoal, self).form_valid(form)

    def create_payment_url(self) -> str:
        """Create payment with Mollie and return payment url"""
        payment_client = MolliePaymentProvider()
        mollie_payment = payment_client.create_payment(self.object)
        payment = payment_client.save_payment_into_db(mollie_payment, self.object)
        return payment.checkout_url
