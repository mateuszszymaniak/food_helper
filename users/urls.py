from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    HomePageView,
    MyLoginView,
    MyResetPasswordView,
    ProfileView,
    RegisterView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path("register/", RegisterView.as_view(), name="register_page"),
    path(
        "login/",
        MyLoginView.as_view(template_name="users/login.html"),
        name="login_page",
    ),
    path("profile/", ProfileView.as_view(), name="profile_page"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout_page",
    ),
    path(
        "reset_password/",
        MyResetPasswordView.as_view(template_name="users/reset_password.html"),
        name="reset_password_page",
    ),
]
