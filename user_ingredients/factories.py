import factory
from factory import SubFactory
from factory.django import DjangoModelFactory

from ingredients.factories import IngredientFactory

from .models import UserIngredient


class UserIngredientFactory(DjangoModelFactory):
    class Meta:
        model = UserIngredient

    ingredient = SubFactory(IngredientFactory)
    amount = factory.Faker("random_int", min=1, max=100)
