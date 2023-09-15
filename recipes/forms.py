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
