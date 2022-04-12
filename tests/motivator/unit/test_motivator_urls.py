"""Unit Tests for testing the urls functionality"""
from django.urls import resolve, reverse


def test_goal_list():
    """
    GIVEN a Django application configured for testing
    WHEN the a path to the goal list is requested
    THEN check that the correct view function is called
    """
    path = reverse("goal-list")

    assert resolve(path).view_name == "goal-list"


def test_goal_details():
    """
    GIVEN a Django application configured for testing
    WHEN the a path to a certain goal detail (pk=1) is requested
    THEN check that the correct view function is called
    """
    path = reverse("goal-detail", kwargs={"pk": 1})

    assert resolve(path).view_name == "goal-detail"


def test_goal_create():
    """
    GIVEN a Django application configured for testing
    WHEN the a path to the create goal is requested
    THEN check that the correct view function is called
    """
    path = reverse("goal-create")

    assert resolve(path).view_name == "goal-create"
