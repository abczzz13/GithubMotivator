"""motivator app URL Configuration"""
from django.urls import path
from .views import index, goals

urlpatterns = [
    path('', index, name='motivator-index'),
    path('goals/', goals, name='motivator-goals')
]
