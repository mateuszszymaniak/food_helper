from django.test import TestCase, tag

from ..factories import IngredientFactory
from ..forms import IngredientsForm


class IngredientFormTest(TestCase):
    def test_valid_recipe_form(self):
        ingredient = IngredientFactory.create()
        ingredient_data = {
            "name": ingredient.name,
            "quantity": ingredient.quantity,
            "quantity_type": ingredient.quantity_type,
        }
        form = IngredientsForm(data=ingredient_data)
        self.assertTrue(form.is_valid())

    def test_invalid_recipe_form(self):
        ingredient = IngredientFactory.create()
        ingredient_data = {
            "quantity": ingredient.quantity,
            "quantity_type": ingredient.quantity_type,
        }
        form = IngredientsForm(data=ingredient_data)
        self.assertFalse(form.is_valid())
