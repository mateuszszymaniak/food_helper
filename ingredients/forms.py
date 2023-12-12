from django import forms

from products.models import Product

from .models import Ingredient


class IngredientsForm(forms.ModelForm):
    product_name = forms.ModelChoiceField(queryset=Product.objects.all())

    class Meta:
        model = Ingredient
        fields = ["amount", "quantity_type"]
