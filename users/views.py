from django.shortcuts import render, redirect
from .forms import UserRegisterForm, MyResetPasswordForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.views import LoginView, AuthenticationForm, PasswordResetView
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from django.forms import ValidationError

# Create your views here.


class CustomAuthForm(AuthenticationForm):
    error_messages = {"invalid_login": "Wrong email or password"}


class MyResetPasswordView(PasswordResetView):
    form_class = MyResetPasswordForm

    def form_valid(self, form):
        if self.request.method == "POST":
            try:
                email_exist = User.objects.get(email=form.data.get("email"))
                same_password = form.data.get("new_password") == form.data.get(
                    "confirm_new_password"
                )
            except Exception:
                messages.warning(self.request, "Email does not exist")
                return redirect("reset_password_page")
            if email_exist and same_password:
                User.objects.filter(email=form.data.get("email")).update(
                    password=make_password(form.data.get("new_password"))
                )
                return redirect("login_page")
            else:
                messages.error(self.request, "Passwords are not the same")
                return redirect("reset_password_page")


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    form_class = CustomAuthForm

    def form_invalid(self, form):
        if self.request.method == "POST":
            try:
                user_exist = User.objects.get(username=form.data.get("username"))
            except Exception:
                user_exist = False
            if user_exist:
                Profile.objects.filter(user=user_exist).update(
                    failed_login_date=datetime.now()
                )
        return redirect("login_page")


def home(request):
    return render(request, "users/home.html", {"title": "Home Page"})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created correctly")
            return redirect("login_page")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"title": "Register", "form": form})


def reset_password(request):
    if request.method == "POST":
        form = MyResetPasswordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password successfully reseted")
            return redirect("login_page")
    else:
        form = MyResetPasswordForm()
    return render(
        request, "users/reset_password.html", {"title": "Reset Password", "form": form}
    )


@login_required
def profile(request):
    return render(request, "users/profile.html", {"title": "Profile"})
