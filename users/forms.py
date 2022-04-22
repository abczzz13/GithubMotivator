import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import UserMotivator


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserMotivatorForm(ModelForm):
    github_username = forms.CharField(min_length=3, max_length=39)

    class Meta:
        model = UserMotivator
        fields = ["github_username"]

    def clean_github_username(self):
        github_username = self.cleaned_data["github_username"]

        if not github_username:
            return github_username

        match = re.search(
            r"^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$", github_username
        )

        if not match:
            self.add_error("github_username", "Invalid username.")

        return github_username


class UserUpdateForm(ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]
