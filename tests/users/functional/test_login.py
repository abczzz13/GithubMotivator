'''End-to-End Tests for testing the login functionality'''
from django.contrib.auth import get_user
import pytest


@pytest.mark.parametrize(
    'username, password, success', [
        ('Test_User', 'PasswordofTestUser', True),
        ('test_user', 'PasswordofTestUser', False),
        ('Test_User', 'passwordoftestuser', False),
        ('Test_User', 'PasswordofTestUserWRONG', False),
        ('Test_User_mispelled', 'PasswordofTestUser', False)
    ]
)
def test_login_parametrized(username, password, success, client, registered_user):
    '''
    GIVEN a Django application configured for testing
    WHEN a POST request is made to login a new user on /login/ with various details
    THEN check that the appropriate response is generated
    '''
    data = {
        'username': username,
        'password': password
    }

    response = client.post('/login/', data)

    logged_in_user = get_user(client)

    assert logged_in_user.is_authenticated == success
    # assert client.session['_auth_user_id'] == '1'
    # assert client.session['_auth_username'] == user['username']
    # assert response.status_code == 302
