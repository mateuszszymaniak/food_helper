from django import forms

from .models import UserIngredient


class UserIngredientForm(forms.ModelForm):
    class Meta:
        model = UserIngredient
        fields = ["amount"]
