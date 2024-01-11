from django.test import TestCase

from ingredients.models import Ingredient
from products.models import Product

from ..factories import RecipeIngredientFactory
from ..models import RecipeIngredient


class TestRecipeIngredientFactory(TestCase):
    def test_create_single_recipe_ingredient(self):
        RecipeIngredientFactory.create()
        self.assertEquals(RecipeIngredient.objects.count(), 1)
        self.assertEquals(Ingredient.objects.count(), 1)
        self.assertEquals(Product.objects.count(), 1)

    def test_multiple_batch_recipe_ingredient(self):
        RecipeIngredientFactory.create_batch(10)
        self.assertEquals(RecipeIngredient.objects.count(), 10)
        self.assertEquals(Ingredient.objects.count(), 10)
        self.assertEquals(Product.objects.count(), 10)
