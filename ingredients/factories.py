import factory

from .models import Ingredient


class IngredientFactory(factory.Factory):
    class Meta:
        model = Ingredient

    name = factory.Faker("word")
    quantity = factory.Faker("random_int", min=1, max=100)
    quantity_type = factory.Iterator(
        [choice[0] for choice in Ingredient.AMOUNT_TYPE_CHOICES]
    )
