import json

from django import forms
from django.forms import formset_factory

from .models import Recipe


class IngredientsForm(forms.Form):
    quantity = forms.CharField(max_length=15)
    name = forms.CharField(max_length=50)


# IngredientFormSet = formset_factory(IngredientsForm)


class CreateNewRecipe(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["recipe_name", "ingredients", "preparation", "tags"]


class RecipeIngredientsForm(forms.Form):
    recipe_form = CreateNewRecipe()
    ingredient_formset = IngredientsForm()

    def save(self, commit=True):
        recipe_name = self.data.get("recipe_name")
        preparation = self.data.get("preparation")
        tags = self.data.get("tags")
        ingredients_list = list(
            filter(lambda key: key.startswith("quantity-"), self.data.keys())
        )
        ingredients_json = {}
        for prefix in ingredients_list:
            quantity = self.data.get(prefix)
            name = self.data.get(f"{prefix.replace('quantity', 'name')}")

            ingredients_json[name] = quantity

        recipe = Recipe(
            recipe_name=recipe_name,
            ingredients=json.dumps(ingredients_json, indent=4, ensure_ascii=False),
            preparation=preparation,
            tags=[tags],
        )

        if commit:
            recipe.save()

        return recipe
