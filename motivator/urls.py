'''Motivator App URL Configuration'''
from django.urls import path
from .views import index, CreateGoal, ListGoal, DetailGoal

urlpatterns = [
    path('', index, name='motivator-index'),
    path('goals/', ListGoal.as_view(), name='goal-list'),
    path('goals/<pk>/', DetailGoal.as_view(), name='goal-detail'),
    path('goals/new', CreateGoal.as_view(), name='goal-create')
]
