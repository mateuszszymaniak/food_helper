import factory
from factory.django import DjangoModelFactory

from .models import Recipe


class RecipeFactory(DjangoModelFactory):
    class Meta:
        model = Recipe

    recipe_name = factory.Faker("word")
    preparation = factory.Faker("text")
    tags = factory.Faker("pylist", nb_elements=1, value_types="word")
