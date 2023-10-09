from django.contrib.auth import views as auth_views
from django.test import SimpleTestCase
from django.urls import resolve, reverse

from users.views import (
    HomePageView,
    MyLoginView,
    MyResetPasswordView,
    ProfileView,
    RegisterView,
)


class TestUrls(SimpleTestCase):
    def test_home_page_url_resolves(self):
        url = reverse("home-page")
        self.assertEquals(resolve(url).func.view_class, HomePageView)

    def test_register_page_url_resolves(self):
        url = reverse("register-page")
        self.assertEquals(resolve(url).func.view_class, RegisterView)

    def test_login_page_url_resolves(self):
        url = reverse("login-page")
        self.assertEquals(resolve(url).func.view_class, MyLoginView)

    def test_profile_page_url_resolves(self):
        url = reverse("profile-page")
        self.assertEquals(resolve(url).func.view_class, ProfileView)

    def test_reset_password_page_url_resolves(self):
        url = reverse("reset-password-page")
        self.assertEquals(resolve(url).func.view_class, MyResetPasswordView)
