'''End-to-End Tests for testing the register functionality'''
from users.models import User
import pytest


@pytest.mark.django_db
def test_register_valid(client):
    '''
    GIVEN a Django application configured for testing
    WHEN a POST request is made to register a new user on /register with valid details
    THEN check that the user is created
    '''
    user = {
        'username': 'Test_User',
        'email': 'test@test.com',
        'password1': 'PasswordofTestUser',
        'password2': 'PasswordofTestUser',
        'github_username': 'testhub'
    }

    response = client.post('/register/', user)

    new_user = User.objects.filter(username=user['username'])

    assert response.status_code == 302
    assert len(new_user) == 1
    assert new_user[0].username == user['username']
    assert new_user[0].email == user['email']
    assert new_user[0].check_password(user['password1'])


@pytest.mark.django_db
def test_register_invalid(client):
    '''
    GIVEN a Django application configured for testing
    WHEN a POST request is made to register a new user on /register with invalid details
    THEN check that the response is invalid
    '''
    user = {
        'username': 'Test User',
        'email': 'test@test.com',
        'password1': '1234',
        'password2': '1234',
        'github_username': ''
    }

    response = client.post('/register/', user)

    new_user = User.objects.filter(username=user['username'])

    assert response.status_code == 200
    assert len(new_user) == 0


@pytest.mark.django_db
def test_register_invalid_github(client):
    '''
    GIVEN a Django application configured for testing
    WHEN a POST request is made to register a new user on /register without a github_username
    THEN check that the response is invalid
    '''
    user = {
        'username': 'Test_User',
        'email': 'test@test.com',
        'password1': 'PasswordofTestUser',
        'password2': 'PasswordofTestUser',
        'github_username': ''
    }

    response = client.post('/register/', user)

    new_user = User.objects.filter(username=user['username'])

    assert response.status_code == 200
    assert len(new_user) == 0


@pytest.mark.django_db
def test_register_invalid_password(client):
    '''
    GIVEN a Django application configured for testing
    WHEN a POST request is made to register a new user on /register with invalid password confirmation
    THEN check that the response is invalid
    '''
    user = {
        'username': 'Test_User',
        'email': 'test@test.com',
        'password1': 'PasswordofTestUser',
        'password2': 'PasswordofTestUserMISTAKE',
        'github_username': 'testhub'
    }

    response = client.post('/register/', user)

    new_user = User.objects.filter(username=user['username'])

    assert response.status_code == 200
    assert len(new_user) == 0
