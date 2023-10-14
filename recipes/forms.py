import re

from django import forms

from .models import Ingredient, Recipe


class IngredientsForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"


class CreateNewRecipe(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["recipe_name", "preparation", "tags"]


class RecipeIngredientsForm(forms.Form):
    recipe_form = CreateNewRecipe()
    ingredient_formset = IngredientsForm()

    def save(self, commit=True):
        recipe_name = self.data.get("recipe_name")
        preparation = self.data.get("preparation")
        tags = self.data.get("tags")
        recipe = Recipe(recipe_name=recipe_name, preparation=preparation, tags=[tags])

        if commit:
            recipe.save()

        return recipe

    def is_valid(self, data):
        name_pattern = any(key for key in data if re.match(r"name-\d+", key))
        quantity_pattern = any(key for key in data if re.match(r"quantity-\d+", key))
        quantity_type_pattern = any(
            key for key in data if re.match(r"quantity_type-\d+", key)
        )
        if name_pattern and quantity_pattern and quantity_type_pattern:
            return super().is_valid()
        else:
            return False
