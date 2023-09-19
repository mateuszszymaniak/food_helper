from datetime import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import AuthenticationForm, LoginView, PasswordResetView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

from .forms import MyResetPasswordForm, UserRegisterForm
from .models import Profile


class CustomAuthForm(AuthenticationForm):
    error_messages = {"invalid_login": "Wrong email or password"}


class MyResetPasswordView(PasswordResetView):
    form_class = MyResetPasswordForm
    success_url = reverse_lazy("login_page")

    def form_valid(self, form):
        email = form.data.get("email")
        new_password = form.data.get("new_password")
        confirm_new_password = form.data.get("confirm_new_password")

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            messages.warning(self.request, "Email does not exist")
            return redirect("reset_password_page")

        if new_password == confirm_new_password:
            user.set_password(new_password)
            user.save()
            messages.success(self.request, "Password successfully reset.")
            return redirect("login_page")
            # return super().form_valid(form) TODO fix later
        else:
            messages.error(self.request, "Passwords are not the same")
            return redirect("reset_password_page")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid form submission")
        return super().form_invalid(form)


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    form_class = CustomAuthForm

    def form_invalid(self, form):
        if self.request.method == "POST":
            username = form.data.get("username")
            user_exist = get_user_model().objects.filter(username=username).exists()
            if user_exist:
                Profile.objects.filter(user=user_exist).update(
                    failed_login_date=datetime.now()
                )
        return redirect("login_page")


class HomePageView(View):
    template_name = "users/home.html"
    context = {"title": "Home Page"}

    def get(self, request):
        return render(request, self.template_name, self.context)


class RegisterView(View):
    template_name = "users/register.html"
    form = UserRegisterForm()
    context = {"title": "Register", "form": form}

    def get(self, request):
        return render(request, self.template_name, self.context)

    @staticmethod
    def post(request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created correctly")
            return redirect("login_page")
        else:
            messages.warning(request, "Form have invalid data")
            return redirect("register_page")


class ResetPasswordView(View):
    template_name = "users/reset_password.html"
    form = MyResetPasswordForm()
    context = {"title": "Reset Password", "form": form}

    def get(self, request):
        return render(request, self.template_name, self.context)

    @staticmethod
    def post(request):
        form = MyResetPasswordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password successfully reseted")
            return redirect("login_page")
        else:
            messages.warning(request, "Form have invalid data")
            return redirect("reset_password_page")


class ProfileView(View):
    template_name = "users/profile.html"
    context = {"title": "Profile"}

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name, self.context)
