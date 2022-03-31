from django import forms
from .models import UserMotivator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserMotivatorForm(ModelForm):
    github_username = forms.CharField(max_length=255)

    class Meta:
        model = UserMotivator
        fields = ['github_username']


class UserUpdateForm(ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
