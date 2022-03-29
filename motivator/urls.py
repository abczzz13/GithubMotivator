"""motivator app URL Configuration"""
from django.urls import path
from .views import index, register, goals

urlpatterns = [
    path('', index, name='motivator-index'),
    path('register/', register, name='motivator-register'),
    path('goals/', goals, name='motivator-goals')
]
