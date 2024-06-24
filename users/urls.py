from django.contrib.auth import views as auth_views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .api.views import APIRegisterView, MyObtainTokenPairView
from .views import (
    HomePageView,
    MyLoginView,
    MyResetPasswordView,
    ProfileView,
    RegisterView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home-page"),
    path("register/", RegisterView.as_view(), name="register-page"),
    path(
        "login/",
        MyLoginView.as_view(template_name="users/login.html"),
        name="login-page",
    ),
    path("profile/", ProfileView.as_view(), name="profile-page"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout-page",
    ),
    path(
        "reset_password/",
        MyResetPasswordView.as_view(template_name="users/reset_password.html"),
        name="reset-password-page",
    ),
    path("api/auth/login/", MyObtainTokenPairView.as_view(), name="token-obtain-view"),
    path("api/auth/login/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/auth/register/", APIRegisterView.as_view(), name="auth-register"),
]
