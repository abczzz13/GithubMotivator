from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView
from mollie.api.error import IdentifierError, RequestError
from users.models import UserMotivator

from motivator.forms import GoalForm
from motivator.models import Goal, Payment
from motivator.payments import MolliePaymentProvider
from motivator.utils_motivator import count_commits


def index(request):
    """View for the homepage of the website"""
    return render(request, "motivator/index.html", {"title": "Home"})


@csrf_exempt
def payment_webhook(request) -> HttpResponse:
    """Payment Webhook for updating the payment status"""
    if "id" not in request.POST:
        return HttpResponse(status=400)

    payment_client = MolliePaymentProvider()
    try:
        updated = payment_client.update_status(request.POST["id"])
    except IdentifierError:
        return HttpResponse(status=400)

    return HttpResponse(status=200) if updated else HttpResponse(status=400)


class ListGoal(LoginRequiredMixin, ListView):
    """Overview of all the Goals"""

    model = Goal
    context_object_name = "goals"

    def get_queryset(self) -> QuerySet[Goal]:
        return self.get_paid_goals()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add context to provide the data to the template"""
        context = super().get_context_data(**kwargs)

        # Add commit count
        context["commit_goals"] = []
        for goal in context["goals"]:
            commit_goal = {"goal": goal, "count": count_commits(goal)}
            context["commit_goals"].append(commit_goal)

        # Add unpaid goals with payment links
        context["unpaid_goals"] = []
        for goal in self.get_unpaid_goals():
            unpaid_goal = {"goal": goal}
            context["unpaid_goals"].append(unpaid_goal)

        return context

    # def get_all_goals(self) -> dict[str, QuerySet[Goal]]:
    #     """"""
    #     user_goals = Goal.objects.filter(user=self.request.user)
    #     paid_payments = Payment.objects.filter(
    #         goal__in=user_goals.values("id"),
    #         payment_status="p",
    #     )
    #     paid_goals = user_goals.filter(id__in=paid_payments.values("goal"))
    #     unpaid_goals = user_goals.exclude(id__in=paid_payments.values("goal"))
    #     return {"paid_goals": paid_goals, "unpaid_goals": unpaid_goals}

    def get_paid_goals(self) -> QuerySet[Goal]:
        """Retrieve all paid goals for current user"""
        user_goals = Goal.objects.filter(user=self.request.user)
        paid_goals = Payment.objects.filter(
            goal__in=user_goals.values("id"),
            payment_status="p",
        )
        return user_goals.filter(id__in=paid_goals.values("goal"))

    def get_unpaid_goals(self) -> QuerySet[Goal]:
        """Retrieve all unpaid goals for current user"""
        user_goals = Goal.objects.filter(user=self.request.user)
        paid_goals = Payment.objects.filter(
            goal__in=user_goals.values("id"),
            payment_status="p",
        )
        return user_goals.exclude(id__in=paid_goals.values("goal"))


class DetailGoal(LoginRequiredMixin, DetailView):
    """View where the user can see the details of a specified Goal"""

    model = Goal
    context_object_name = "goal"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add context to provide the data to the template"""
        context = super().get_context_data(**kwargs)

        # Add commit count
        context["commit_count"] = count_commits(context["goal"])

        # Add payment status
        for payment in self.get_payments():
            if payment.payment_status == "p":
                context["unpaid"] = False
                return context
        context["unpaid"] = True
        return context

    def get_payments(self) -> QuerySet[Payment]:
        """Retrieves all the payments related to the Goal"""
        return Payment.objects.filter(goal=self.object)


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
        return reverse("get-payment-link", args=[self.object.pk])

    def form_valid(self, form):
        """Adds the extra fields to save in the Model"""
        form.instance.user = self.request.user
        form.instance.github_username = self.github_username
        return super(CreateGoal, self).form_valid(form)


def get_payment_link(request, pk: int) -> HttpResponse:
    """Retrieves or creates the Mollie payment link"""
    goal = Goal.objects.filter(id=pk).first()
    if goal is None:
        return redirect("goal-list")
    payment_client = MolliePaymentProvider()
    try:
        payment_link = payment_client.get_or_create_payment_link(goal)
    except RequestError:
        return render(request, "motivator/payment_error.html", {"title": "Payment Error"})
    return redirect(payment_link)
