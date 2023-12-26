from django.db import models

from ingredients.models import Ingredient


class RecipeIngredients(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.ingredient}, {self.amount}"

    # TODO add user in future
