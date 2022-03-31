from django.db import models
from django.contrib.auth.models import User


class UserMotivator(models.Model):
    '''Extending the Django User Model'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github_username = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username} Profile'
