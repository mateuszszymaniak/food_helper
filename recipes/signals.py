from django.db.models.signals import pre_delete
from django.dispatch import receiver

from recipes.models import Recipe


@receiver(pre_delete, sender=Recipe)
def pre_delete_recipe(sender, instance, **kwargs):
    ingredients = instance.recipe_ingredient.all()

    for ingredient in ingredients:
        ingredient.delete()
