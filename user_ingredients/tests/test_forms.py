from django.test import TestCase

from ..forms import UserIngredientForm


class UserIngredientTest(TestCase):
    def test_valid_user_ingredient_form(self):
        user_ingredient_data = {
            "amount": 1,
        }
        form = UserIngredientForm(data=user_ingredient_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_ingredient_form_both_wrong(self):
        user_ingredient_data = {
            "amount": 0,
        }
        form = UserIngredientForm(data=user_ingredient_data)
        self.assertFalse(form.is_valid())
