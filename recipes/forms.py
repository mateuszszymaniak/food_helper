from django import forms

from .models import Recipe


class CreateNewRecipe(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["recipe_name", "preparation"]

    def __init__(self, *args, **kwargs):
        super(CreateNewRecipe, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "recipe_name":
                field.required = False


class EditRecipe(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["recipe_name", "preparation"]

    def __init__(self, *args, **kwargs):
        super(EditRecipe, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "recipe_name":
                field.required = False
