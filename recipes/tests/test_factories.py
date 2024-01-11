from django.test import TestCase

from ..factories import RecipeFactory
from ..models import Recipe


class TestRecipeFactory(TestCase):
    def test_create_single_recipe(self):
        RecipeFactory.create()
        self.assertEquals(Recipe.objects.count(), 1)

    def test_multiple_batch_recipe(self):
        RecipeFactory.create_batch(10)
        self.assertEquals(Recipe.objects.count(), 10)
