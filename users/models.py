from django.db import models
from django.contrib.auth.models import User


class Users(User):
    '''Extending the Django User Model'''
    github_username = models.CharField(max_length=255)
