# from django.contrib.postgres.fields import ArrayField
from django.db import models

from recipe_ingredients.models import RecipeIngredient
from users.models import Profile


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=100, unique=True)
    preparation = models.TextField(blank=False, default="")
    recipe_ingredient = models.ManyToManyField(RecipeIngredient)
    # tags = ArrayField(models.CharField(max_length=20, null=True), blank=True, null=True)
    user = models.ForeignKey(
        Profile, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    builtin = models.BooleanField(default=False)
    public = models.BooleanField(default=True)
