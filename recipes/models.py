from django.contrib.postgres.fields import ArrayField
from django.db import models

from ingredients.models import Ingredient
from users.models import Profile


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=100)
    preparation = models.TextField(blank=False, default="")
    ingredients = models.ManyToManyField(Ingredient)
    tags = ArrayField(models.CharField(max_length=20, null=True), blank=True, null=True)
    user = models.ForeignKey(
        Profile, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    builtin = models.BooleanField(default=False)
    public = models.BooleanField(default=True)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    # TODO add user in future
