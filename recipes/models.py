from django.contrib.postgres.fields import ArrayField
from django.db import models

from ingredients.models import Ingredient
from users.models import Profile


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=100)
    preparation = models.TextField(blank=False, default="")
    tags = ArrayField(models.CharField(max_length=20, null=True), blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="recipes")


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    # TODO add user in future
