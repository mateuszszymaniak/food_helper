from django.test import TestCase, tag

from ..factories import RecipeFactory
from ..forms import CreateNewRecipe


class RecipeFormTest(TestCase):
    def test_valid_recipe_form(self):
        recipe = RecipeFactory.create()
        recipe_data = {
            "recipe_name": recipe.recipe_name,
            "preparation": recipe.preparation,
            "tags": recipe.tags,
        }
        form = CreateNewRecipe(data=recipe_data)
        self.assertTrue(form.is_valid())

    def test_invalid_recipe_form(self):
        recipe = RecipeFactory.create()
        recipe_data = {"recipe_name": recipe.recipe_name, "tags": recipe.tags}
        form = CreateNewRecipe(data=recipe_data)
        self.assertFalse(form.is_valid())
