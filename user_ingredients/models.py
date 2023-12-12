from django.db import models

from ingredients.models import Ingredient
from users.models import Profile


class UserIngredient(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.DO_NOTHING, null=False, blank=False
    )
    ingredients = models.ForeignKey(
        Ingredient, on_delete=models.DO_NOTHING, null=False, blank=False
    )
    amount = models.PositiveIntegerField()
