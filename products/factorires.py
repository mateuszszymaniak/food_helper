import factory
from factory.django import DjangoModelFactory

from .models import Product


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("word")
