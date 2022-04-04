from django.urls import reverse, resolve


class TestUsersUrls:

    def test_register(self):
        path = reverse('users-register')

        assert resolve(path).view_name == 'users-register'

    def test_login(self):
        path = reverse('login')

        assert resolve(path).view_name == 'login'

    def test_logout(self):
        path = reverse('logout')

        assert resolve(path).view_name == 'logout'

    def test_profile(self):
        path = reverse('users-profile')

        assert resolve(path).view_name == 'users-profile'

    def test_password_reset(self):
        path = reverse('password_reset')

        assert resolve(path).view_name == 'password_reset'

    def test_password_reset_done(self):
        path = reverse('password_reset_done')

        assert resolve(path).view_name == 'password_reset_done'

    def test_password_reset_confirm(self):
        path = reverse('password_reset_confirm', kwargs={
                       'uidb64': 1, 'token': 'abcdefgh'})

        assert resolve(path).view_name == 'password_reset_confirm'

    def test_password_reset_complete(self):
        path = reverse('password_reset_complete')

        assert resolve(path).view_name == 'password_reset_complete'
