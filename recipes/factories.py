import random

import factory

from .models import Ingredient, Recipe


class IngredientFactory(factory.Factory):
    class Meta:
        model = Ingredient

    name = factory.Faker("word")
    quantity = factory.Faker("random_int", min=1, max=100)
    quantity_type = factory.Iterator(
        [choice[0] for choice in Ingredient.AMOUNT_TYPE_CHOICES]
    )


class RecipeFactory(factory.Factory):
    class Meta:
        model = Recipe

    recipe_name = factory.Faker("word")
    preparation = factory.Faker("text")
    tags = factory.Faker("word")
