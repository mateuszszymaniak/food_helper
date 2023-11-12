from django import forms

from .models import Ingredient


class IngredientsForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "quantity", "quantity_type"]
