from django import forms
from .models import Users
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    github_username = forms.CharField(max_length=255)

    class Meta:
        model = Users
        fields = ['username', 'email',
                  'github_username', 'password1', 'password2']
