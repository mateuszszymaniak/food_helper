from django import forms

from products.models import Product

from .models import Ingredient


class IngredientsForm(forms.ModelForm):
    amount = forms.IntegerField(min_value=1)
    product_name = forms.ModelChoiceField(queryset=Product.objects.all())

    class Meta:
        model = Ingredient
        fields = ["amount", "product_name", "quantity_type"]

    def __init__(self, *args, **kwargs):
        super(IngredientsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False

    def is_valid(self):
        filled_amount = self.data.get("amount")
        filled_quantity_type = self.data.get("quantity_type")
        filled_product_name = self.data.get("product_name")
        if filled_amount and filled_quantity_type and filled_product_name:
            return super().is_valid()
        else:
            return False
