import factory

from .models import Recipe


class RecipeFactory(factory.Factory):
    class Meta:
        model = Recipe

    recipe_name = factory.Faker("word")
    preparation = factory.Faker("text")
    tags = factory.Faker("word")
