from http import HTTPStatus

from django.test import TestCase, tag
from django.urls import reverse

from users.models import Profile, User

HOME_PAGE = "home-page"


# @tag('x')
class TestViews(TestCase):
    def setUp(self):
        self.home_page = reverse("home-page")
        self.login_page = reverse("login-page")
        self.register_page = reverse("register-page")
        self.reset_password_page = reverse("reset-password-page")
        self.profile_page = reverse("profile-page")
        self.user_username = "user1"
        self.user_password = "pass1!"  # nosec bandit B105
        self.user_email = "email@email.pl"
        self.user1 = User.objects.create(
            username=self.user_username,
            email=self.user_email,
        )
        self.user1.set_password(self.user_password)
        self.user1.save()
        self.profile1 = Profile.objects.get(user=self.user1)

    # region tests for home view
    def test_home_page_view_GET(self):
        """
        user is not logged
        """
        response = self.client.get(self.home_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/home.html")
        self.assertContains(response, "Login")

        """
        logged user
        """
        self.client.login(username=self.user_username, password=self.user_password)
        response = self.client.get(self.home_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/dashboard.html")

    # endregion
    # region tests for login view
    def test_login_page_view_GET(self):
        response = self.client.get(self.login_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_page_view_POST_incorrect_credentials(self):
        """
        username and password are incorrect
        """
        login_data = {"username": "", "password": ""}
        response = self.client.post(self.login_page, login_data)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, expected_url=self.login_page)

        """
        username is correct, password incorrect
        """
        login_data = {"username": "user1", "password": "test_pass"}
        response = self.client.post(self.login_page, login_data)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, expected_url=self.login_page)

        """
        username is incorrect, password is correct
        """
        login_data = {"username": "test_user", "password": "pass1!"}
        response = self.client.post(self.login_page, login_data)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, expected_url=self.login_page)

    def test_login_page_view_POST_correct_credentials(self):
        login_data = {"username": "user1", "password": "pass1!"}
        response = self.client.post(self.login_page, login_data)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, expected_url=self.home_page)

    # endregion
    # region tests for register view
    def test_register_page_view_GET(self):
        response = self.client.get(self.register_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register.html")

    def test_register_page_view_POST_correct_data(self):
        initial_count = User.objects.count()

        register_data = {
            "username": "Test001",
            "email": "tyu@tyu.tyu",
            "password1": "Tyu123!@#",
            "password2": "Tyu123!@#",
        }
        response = self.client.post(self.register_page, register_data)
        final_count = User.objects.count()
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, expected_url=self.login_page)
        self.assertEquals(final_count, initial_count + 1)

    def test_register_page_view_POST_incorrect_data(self):
        """
        the same user as in database
        """
        register_data = {
            "username": "user1",
            "email": "zxc@zxc.zxc",
            "password1": "Asd123!@#",
            "password2": "Asd123!@#",
        }
        response = self.client.post(self.register_page, register_data)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, expected_url=self.register_page)

        """
        the same email as in database
        """
        register_data = {
            "username": "hjk1",
            "email": "email@email.pl",
            "password1": "Vbg123!",
            "password2": "Vbg123!",
        }
        response = self.client.post(self.register_page, register_data)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, expected_url=self.register_page)

        """
        different password
        """
        register_data = {
            "username": "rrr1",
            "email": "rrr@rr.rr",
            "password1": "rrr123!",
            "password2": "rrr123!!",
        }
        response = self.client.post(self.register_page, register_data)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, expected_url=self.register_page)

    # endregion
    # region tests for reset_password view
    def test_reset_password_page_view_GET(self):
        response = self.client.get(self.reset_password_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/reset_password.html")

    def test_reset_password_page_view_POST_correct_data(self):
        reset_password_data = {
            "email": "email@email.pl",
            "new_password": "q",
            "confirm_new_password": "q",
        }
        response = self.client.post(self.reset_password_page, reset_password_data)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, expected_url=self.login_page)

    def test_reset_password_page_view_POST_incorrect_data(self):
        """
        email does not exist
        """
        reset_password_data = {
            "email": "ee@ee.ee",
            "new_password": "e",
            "confirm_new_password": "e",
        }
        response = self.client.post(self.reset_password_page, reset_password_data)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, expected_url=self.reset_password_page)

        """
        different passwords
        """
        reset_password_data = {
            "email": "email@email.pl",
            "new_password": "p",
            "confirm_new_password": "q",
        }
        response = self.client.post(self.reset_password_page, reset_password_data)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, expected_url=self.reset_password_page)

    # endregion
    # region tests for profile view
    def test_profile_view_GET(self):
        """
        user is not logged
        """
        response = self.client.get(self.profile_page)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertIn("/login/", response.url)

        """
        user logged
        """
        log_in = self.client.login(
            username=self.user_username, password=self.user_password
        )
        self.assertTrue(log_in)
        response = self.client.get(self.profile_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/profile.html")

    # endregion
