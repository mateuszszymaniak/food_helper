from django import forms

from .models import RecipeIngredients


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredients
        fields = ["amount"]
