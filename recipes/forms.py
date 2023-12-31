from django import forms

from .models import Recipe


class CreateNewRecipe(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["recipe_name", "preparation", "tags"]

    def __init__(self, *args, **kwargs):
        super(CreateNewRecipe, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False

    def is_valid(self):
        filled_recipe_name = self.data.get("recipe_name")
        if filled_recipe_name:
            return super().is_valid()
        else:
            return False
