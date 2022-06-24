from typing import Any

from django.conf import settings
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

from .forms import GoalForm
from .models import Goal, Payment
from .payments import MolliePaymentProvider
from .utils_motivator import count_commits


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
    try:
        payment = payment_client.get_payment_info(id)
    except IdentifierError:
        return HttpResponse(status=400)

    if payment["id"] == id and payment["profileId"] == settings.MOLLIE_PROFILE_ID:
        Payment.objects.filter(mollie_id=id).update(
            payment_status=Payment.process_payment_status(payment["status"])
        )

    return HttpResponse(status=200)


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

        # Add unpaid goals with payment links
        # context["unpaid_goals"] = []
        # for goal in self.get_unpaid_goals():
        #     unpaid_goal = {"goal": goal}
        #     try:
        #         unpaid_goal["payment_link"] = MolliePaymentProvider.get_or_create_payment(goal)
        #     except RequestError:
        #         unpaid_goal["error"] = "Error with creating payment"
        #     context["unpaid_goals"].append(unpaid_goal)

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

        # Add payment link if unpaid
        # payments = self.get_payments()
        # for payment in payments:
        #     if payment.payment_status == "p":
        #         return context
        #     if payment.payment_status == "o":
        #         context["payment_link"] = payment.checkout_url

        # if "payment_link" not in context:
        #     try:
        #         context["payment_link"] = MolliePaymentProvider.get_or_create_payment(self.object)
        #     except RequestError:
        #         context["error"] = "Error with creating payment"
        # return context

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
        # return self.create_payment_url()
        return reverse("get-payment-link", args=[self.object.pk])

    def form_valid(self, form):
        """Adds the extra fields to save in the Model"""
        form.instance.user = self.request.user
        form.instance.github_username = self.github_username
        return super(CreateGoal, self).form_valid(form)

    # def create_payment_url(self) -> str:
    #     """Create payment with Mollie and return payment url"""
    #     payment_client = MolliePaymentProvider()
    #     try:
    #         payment = payment_client.create_payment(self.object)
    #         return payment.checkout_url
    #     except RequestError:
    #         # What to do in this situation?
    #         return redirect("goal-list")


def get_payment_link(request, pk: int) -> HttpResponse:
    """Retrieves or creates the Mollie payment link"""
    goal = Goal.objects.filter(id=pk).first()
    if goal is None:
        return redirect("goal-list")
    payment_client = MolliePaymentProvider()
    try:
        payment_link = payment_client.get_or_create_payment(goal)
    except RequestError:
        # What to do in this situation?
        # maybe a seperate fallback page?
        return redirect("goal-list")
    return redirect(payment_link)
