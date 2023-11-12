from django import forms

from .models import Recipe


class CreateNewRecipe(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["recipe_name", "preparation", "tags"]
