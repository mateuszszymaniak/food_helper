import json

from django import forms
from .models import Recepie
from django.forms import formset_factory


class IngredientsForm(forms.Form):
    quantity = forms.CharField(max_length=15)
    name = forms.CharField(max_length=50)


# IngredientFormSet = formset_factory(IngredientsForm)


class CreateNewRecepie(forms.ModelForm):
    class Meta:
        model = Recepie
        fields = ["recepie_name", "ingredients", "preparation", "tags"]


class RecepieIngredientsForm(forms.Form):
    recepie_form = CreateNewRecepie()
    ingredient_formset = IngredientsForm()

    def save(self, commit=True):
        recepie_name = self.data.get("recepie_name")
        preparation = self.data.get("preparation")
        tags = self.data.get("tags")
        ingredients_amount = len(
            list(filter(lambda key: key.startswith("quantity-"), self.data.keys()))
        )
        ingredients_json = {}
        for prefix in range(ingredients_amount):
            quantity = self.data.get(f"quantity-{prefix}")
            name = self.data.get(f"name-{prefix}")
            if quantity and name:
                ingredients_json[name] = quantity
        # for var in list(self.data.keys()):
        #     if "quantity-" in var:
        #         ingredients_json = {'quantity': self.data.get(var)}
        #     elif "name-" in var:
        #         ingredients_json = {"name": self.data.get(var)}

        recepie = Recepie(
            recepie_name=recepie_name,
            ingredients=json.dumps(ingredients_json, indent=4, ensure_ascii=False),
            preparation=preparation,
            tags=[tags],
        )

        if commit:
            recepie.save()

        return recepie
