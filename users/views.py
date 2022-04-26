from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserMotivatorForm, UserUpdateForm


def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        motivator_form = UserMotivatorForm(request.POST)
        if user_form.is_valid() and motivator_form.is_valid():
            user = user_form.save()
            motivator = motivator_form.save(commit=False)
            motivator.user = user
            motivator.save()
            messages.success(request, "Your account has been created. You can now login")

            return HttpResponseRedirect("/login")
        else:
            return render(request, "users/register.html", {"user_form": user_form, "motivator_form": motivator_form})
    else:
        user_form = UserRegisterForm()
        motivator_form = UserMotivatorForm()

        context = {"title": "Register", "user_form": user_form, "motivator_form": motivator_form}

    return render(request, "users/register.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        motivator_form = UserMotivatorForm(request.POST, instance=request.user.usermotivator)

        if user_update_form.is_valid() and motivator_form.is_valid():
            user = user_update_form.save()
            motivator = motivator_form.save(commit=False)
            motivator.user = user
            motivator.save()
            messages.success(request, "Your account has been updated.")

            return HttpResponseRedirect("/profile")
        else:
            return render(
                request, "users/profile.html", {"user_update_form": user_update_form, "motivator_form": motivator_form}
            )

    else:
        user_update_form = UserUpdateForm(instance=request.user)
        motivator_form = UserMotivatorForm(instance=request.user.usermotivator)

        context = {"user_update_form": user_update_form, "motivator_form": motivator_form}

    return render(request, "users/profile.html", context)
