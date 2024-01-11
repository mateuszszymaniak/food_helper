from django.core.validators import MinValueValidator
from django.db import models

from ingredients.models import Ingredient


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.ingredient}, {self.amount}"

    # TODO add user in future
