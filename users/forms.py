from django import forms
from django.contrib.auth.forms import PasswordResetForm, User, UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class MyResetPasswordForm(PasswordResetForm):
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_new_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["email"]
