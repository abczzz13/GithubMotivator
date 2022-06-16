from typing import Any

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView
from mollie.api.client import Client
from users.models import UserMotivator

from .forms import GoalForm
from .models import Goal, Payment
from .utils_motivator import count_commits


def index(request):
    """View for the homepage of the website"""
    return render(request, "motivator/index.html", {"title": "Home"})


@csrf_exempt
def mollie_webhook(request) -> JsonResponse:
    """Mollie Webhook for updating the payment status"""
    if "id" not in request.POST:
        return JsonResponse({"response": "Error! No id found"})
    payment_id = request.POST["id"]

    mollie_client = Client()
    mollie_client.set_api_key(settings.MOLLIE_API_KEY)

    payment = mollie_client.payments.get(payment_id)
    Payment.objects.filter(mollie_id=payment_id).update(
        payment_status=Payment.process_payment_status(payment["status"])
    )
    return JsonResponse({"response": "Success!"})


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
        """Starts the Mollie payment process and redirects to the Mollie payment url"""
        payment_url = self.start_payment()
        return payment_url

    def form_valid(self, form):
        """Adds the extra fields to save in the Model"""
        form.instance.user = self.request.user
        form.instance.github_username = self.github_username
        return super(CreateGoal, self).form_valid(form)

    def amount_to_str(self, amount: int) -> str:
        """Convert amount to a str for creating a Mollie payment"""
        return str(f"{amount:.2f}")

    def start_payment(self) -> str:
        """Create payment with Mollie and return payment url"""
        mollie_client = Client()
        mollie_client.set_api_key(settings.MOLLIE_API_KEY)

        payload = {
            "amount": {
                "currency": "EUR",
                "value": self.amount_to_str(self.object.amount),
            },
            "description": f"Goal #{self.object.pk} ",
            "redirectUrl": "http://localhost:8000/goals/",
            "webhookUrl": f"{settings.MOLLIE_PUBLIC_URL}/mollie/",
            "metadata": {
                "goal_id": self.object.pk,
                "user_id": self.object.user.id,
            },
        }
        mollie_payment = mollie_client.payments.create(payload)

        payment = Payment(
            mollie_id=mollie_payment["id"],
            amount_eur=mollie_payment["amount"]["value"],
            checkout_url=mollie_payment["_links"]["checkout"]["href"],
            payment_status="o",
            goal=self.object,
        )
        payment.save()
        return payment.checkout_url
