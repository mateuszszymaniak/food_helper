from django.test import TestCase

from products.models import Product

from ..factories import IngredientFactory
from ..models import Ingredient


class TestIngredientFactory(TestCase):
    def test_create_single_ingredient(self):
        IngredientFactory.create()
        self.assertEquals(Ingredient.objects.count(), 1)
        self.assertEquals(Product.objects.count(), 1)

    def test_multiple_batch_ingredient(self):
        IngredientFactory.create_batch(10)
        self.assertEquals(Ingredient.objects.count(), 10)
        self.assertEquals(Product.objects.count(), 10)
