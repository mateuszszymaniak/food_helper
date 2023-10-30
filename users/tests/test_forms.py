from django.test import TestCase, tag

from ..factories import UserFactory
from ..forms import UserRegisterForm


class UserRegisterFormTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()

    @tag("x")
    def test_valid_user_register_form(self):
        user = UserFactory.create()
        form_data = {
            "username": self.user.username,
            "email": self.user.email,
            "password1": self.user.password,
            "password2": self.user.password,
        }

        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_register_form(self):
        form_data = {
            "username": "testuser",
            "email": "invalid_email",
            "password1": "mypassword123",
            "password2": "differentpassword",
        }

        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
