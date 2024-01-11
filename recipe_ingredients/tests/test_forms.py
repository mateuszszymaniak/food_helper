from django.test import TestCase

from ..forms import RecipeIngredientForm


class RecipeIngredientTest(TestCase):
    def test_valid_user_ingredient_form(self):
        recipe_ingredient_data = {
            "amount": 1,
        }
        form = RecipeIngredientForm(data=recipe_ingredient_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_ingredient_form_both_wrong(self):
        recipe_ingredient_data = {
            "amount": 0,
        }
        form = RecipeIngredientForm(data=recipe_ingredient_data)
        self.assertFalse(form.is_valid())
