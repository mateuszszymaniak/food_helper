import factory

from ingredients.factories import IngredientFactory

from .models import UserIngredient


class UserIngredientFactory(factory.Factory):
    class Meta:
        model = UserIngredient

    ingredients = IngredientFactory.create()
    amount = factory.Faker("random_int", min=1, max=100)
