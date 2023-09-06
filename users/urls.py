from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import MyLoginView, MyResetPasswordView

urlpatterns = [
    path("", views.home, name="home_page"),
    path("register/", views.register, name="register_page"),
    path(
        "login/",
        MyLoginView.as_view(template_name="users/login.html"),
        name="login_page",
    ),
    path("profile/", views.profile, name="profile_page"),
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
