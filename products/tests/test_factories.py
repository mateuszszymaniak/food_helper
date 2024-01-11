from django.test import TestCase

from ..factorires import ProductFactory
from ..models import Product


class TestProductFactory(TestCase):
    def test_create_single_recipe_ingredient(self):
        ProductFactory.create()
        self.assertEquals(Product.objects.count(), 1)

    def test_multiple_batch_product(self):
        ProductFactory.create_batch(10)
        self.assertEquals(Product.objects.count(), 10)
