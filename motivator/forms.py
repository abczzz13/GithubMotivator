from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='E-mail', max_length=255)
    # password = forms.PasswordInput()
