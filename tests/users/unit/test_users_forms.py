"""Unit Tests for testing the Users Forms"""
import pytest
from users.forms import UserMotivatorForm, UserRegisterForm, UserUpdateForm

username = "Test_User"
password = "TheWarOnDrugs"
email = "test@test.com"


@pytest.mark.django_db
def test_register_form_valid():
    """
    GIVEN a Django application configured for testing
    WHEN valid data is used as input to the User Register Form
    THEN confirm the that form validation returns a valid repsonse
    """
    form_data = {
        "username": username,
        "password1": password,
        "password2": password,
        "email": email,
    }

    form = UserRegisterForm(data=form_data)
    assert form.is_valid()


@pytest.mark.parametrize(
    "field, value, error",
    [
        ("username", "", "This field is required."),
        ("password1", "", "This field is required."),
        ("password2", "", "This field is required."),
        ("email", "", "This field is required."),
        (
            "username",
            "Test User",
            "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.",
        ),
        ("email", "@gmail.com", "Enter a valid email address."),
    ],
)
@pytest.mark.django_db
def test_register_form_invalid(field, value, error):
    """
    GIVEN a Django application configured for testing
    WHEN invalid data is used as input to the User Register Form
    THEN confirm the that correct error responses are returned
    """
    form_data = {
        "username": username,
        "password1": password,
        "password2": password,
        "email": email,
    }
    form_data[field] = value

    form = UserRegisterForm(data=form_data)

    assert form.errors[field] == [error]


def test_motivator_form_valid():
    """
    GIVEN a Django application configured for testing
    WHEN valid data is used as input to the User Motivator Form
    THEN confirm the that form validation returns a valid repsonse
    """
    form_data = {
        "github_username": "abczzz13",
    }

    form = UserMotivatorForm(data=form_data)

    assert form.is_valid()


@pytest.mark.parametrize(
    "github_username, error",
    [
        ("", "This field is required."),
        ("a_b", "Invalid username."),
        ("-abc", "Invalid username."),
        ("abc-", "Invalid username."),
        ("ab", "Ensure this value has at least 3 characters (it has 2)."),
        (
            "abcde" * 8,
            "Ensure this value has at most 39 characters (it has 40).",
        ),
    ],
)
def test_motivator_form_invalid(github_username, error):
    """
    GIVEN a Django application configured for testing
    WHEN invalid data is used as input to the User Motivator Form
    THEN confirm the that correct error responses are returned
    """
    form_data = {
        "github_username": github_username,
    }

    form = UserMotivatorForm(data=form_data)
    form.is_valid()

    assert form.errors["github_username"] == [error]


@pytest.mark.parametrize(
    "username, email, assertion",
    [
        (username, email, True),
        ("Test User", email, False),
        (username, "test@test", False),
        ("", email, False),
        (username, "", False),
    ],
)
@pytest.mark.django_db
def test_update_form(username, email, assertion):
    """
    GIVEN a Django application configured for testing
    WHEN data is used as input to the User Update Form
    THEN that the data gets correctly validated
    """
    form_data = {
        "username": username,
        "email": email,
    }

    form = UserUpdateForm(data=form_data)

    assert form.is_valid() is assertion
