from django.contrib.auth.forms import UserChangeForm, AuthenticationForm, UserCreationForm
from mainapp.models import Buyer
from django import forms


class LoginForm(AuthenticationForm):
    class Meta:
        model = Buyer
        fields = ('email', 'password')


class RegisterForm(UserCreationForm):
    class Meta:
        model = Buyer
        fields = ('email', 'password1', 'password2', 'username')
