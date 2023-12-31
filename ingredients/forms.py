from django import forms

from products.models import Product

from .models import Ingredient


class IngredientForm(forms.ModelForm):
    product_name = forms.ModelChoiceField(queryset=Product.objects.all())

    class Meta:
        model = Ingredient
        fields = ["product_name", "quantity_type"]
