from django.test import TestCase

from ..forms import CreateNewRecipe


class RecipeFormTest(TestCase):
    def test_valid_recipe_form(self):
        recipe_data = {
            "recipe_name": "xyz",
            "preparation": "asd",
            # "tags": "tyu",
        }
        form = CreateNewRecipe(data=recipe_data)
        self.assertTrue(form.is_valid())

    def test_invalid_recipe_form(self):
        recipe_data = {}
        form = CreateNewRecipe(data=recipe_data)
        self.assertFalse(form.is_valid())
