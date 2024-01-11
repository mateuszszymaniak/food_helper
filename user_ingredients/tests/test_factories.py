from django.test import TestCase

from ingredients.models import Ingredient
from products.models import Product
from users.factories import UserFactory
from users.models import Profile

from ..factories import UserIngredientFactory
from ..models import UserIngredient


class TestUserIngredientsFactory(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.profile, _ = Profile.objects.get_or_create(user=self.user)

    def test_create_single_user_ingredient(self):
        UserIngredientFactory.create(user=self.profile)
        self.assertEquals(UserIngredient.objects.count(), 1)
        self.assertEquals(Ingredient.objects.count(), 1)
        self.assertEquals(Product.objects.count(), 1)

    def test_multiple_batch_user_ingredient(self):
        UserIngredientFactory.create_batch(10, user=self.profile)
        self.assertEquals(UserIngredient.objects.count(), 10)
        self.assertEquals(Ingredient.objects.count(), 10)
        self.assertEquals(Product.objects.count(), 10)
