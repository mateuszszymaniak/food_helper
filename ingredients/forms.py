from django import forms

from products.models import Product

from .models import Ingredient


class IngredientsForm(forms.ModelForm):
    amount = forms.IntegerField(min_value=1)
    product_name = forms.ModelChoiceField(queryset=Product.objects.all())

    class Meta:
        model = Ingredient
        fields = ["amount", "product_name", "quantity_type"]
