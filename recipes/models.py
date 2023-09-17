from django.contrib.postgres.fields import ArrayField
from django.db import models

from users.models import Profile


class Ingredient(models.Model):
    AMOUNT_TYPE_CHOICES = (
        ("", ""),
        ("kg", "kg"),
        ("g", "g"),
        ("l", "l"),
        ("ml", "ml"),
        ("szt.", "szt."),
        ("opak.", "opak."),
    )

    name = models.CharField(max_length=50)
    quantity = models.CharField(max_length=5)
    quantity_type = models.CharField(
        max_length=5, choices=AMOUNT_TYPE_CHOICES, default=""
    )
    # TODO add user in future


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=100)
    preparation = models.TextField(blank=False, default="")
    tags = ArrayField(models.CharField(max_length=20, null=True), blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    # TODO add user in future
