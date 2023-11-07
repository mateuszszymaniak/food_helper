from django.test import TestCase, tag

from ..factories import UserFactory
from ..forms import UserRegisterForm


class UserRegisterFormTest(TestCase):
    def test_valid_user_register_form(self):
        form_data = {
            "username": "Xyz123",
            "email": "xyz123@xyz.pl",
            "password1": "Test123!",
            "password2": "Test123!",
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
