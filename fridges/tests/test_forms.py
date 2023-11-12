from django.test import TestCase, tag

from ingredients.factories import IngredientFactory

from ..forms import NewIngredientForm


class FridgeFormTest(TestCase):
    def test_valid_fridge_form(self):
        ingredient = IngredientFactory.create()
        ingredient_data = {
            "name": ingredient.name,
            "quantity": ingredient.quantity,
            "quantity_type": ingredient.quantity_type,
        }
        form = NewIngredientForm(data=ingredient_data)
        self.assertTrue(form.is_valid())

    def test_invalid_fridge_form(self):
        ingredient_data = {}
        form = NewIngredientForm(data=ingredient_data)
        self.assertFalse(form.is_valid())
