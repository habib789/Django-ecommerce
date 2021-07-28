from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms


class UserForm(UserCreationForm):
    class Meta:
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'Enter Full Name'
        self.fields['email'].label = 'Enter your email'


class UserUpdateForm(UserChangeForm):
    class Meta:
        fields = ['username', 'first_name', 'email']
        model = User


class ChangePassForm(PasswordChangeForm):
    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']
        model = User
