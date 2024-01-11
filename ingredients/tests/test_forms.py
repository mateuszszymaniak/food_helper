from django.test import TestCase

from products.factorires import ProductFactory

from ..forms import IngredientForm


class IngredientFormTest(TestCase):
    def setUp(self):
        self.product = ProductFactory.create()

    def test_valid_recipe_form(self):
        ingredient_data = {
            "product_name": self.product.id,
            "quantity_type": "kg",
        }
        form = IngredientForm(data=ingredient_data)
        self.assertTrue(form.is_valid())

    def test_invalid_recipe_form_both_wrong(self):
        ingredient_data = {
            "quantity": "qwe",
            "quantity_type": "abc",
        }
        form = IngredientForm(data=ingredient_data)
        self.assertFalse(form.is_valid())

    def test_invalid_recipe_form_quality_wrong(self):
        ingredient_data = {
            "quantity": "qwe",
            "quantity_type": "l",
        }
        form = IngredientForm(data=ingredient_data)
        self.assertFalse(form.is_valid())

    def test_invalid_recipe_form_wrong_quantity_type(self):
        ingredient_data = {
            "quantity": "1",
            "quantity_type": "xer",
        }
        form = IngredientForm(data=ingredient_data)
        self.assertFalse(form.is_valid())
