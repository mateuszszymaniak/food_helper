import factory
from factory import SubFactory
from factory.django import DjangoModelFactory

from products.factorires import ProductFactory

from .models import Ingredient


class IngredientFactory(DjangoModelFactory):
    class Meta:
        model = Ingredient

    product = SubFactory(ProductFactory)
    quantity_type = factory.Iterator(
        [choice[0] for choice in Ingredient.AMOUNT_TYPE_CHOICES]
    )
