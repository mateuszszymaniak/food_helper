from django import forms

from .models import Fridge


class NewIngredientForm(forms.ModelForm):
    class Meta:
        model = Fridge
        fields = ["name", "quantity", "quantity_type"]
