from django.test import SimpleTestCase
from django.urls import resolve, reverse

from recipe_ingredients.views import (
    RecipeIngredientAddView,
    RecipeIngredientDeleteView,
    RecipeIngredientEditView,
)


class TestUrls(SimpleTestCase):
    def test_ingredient_add_url_resolves(self):
        url = reverse("ingredients:ingredient-add", args=[1])
        self.assertEquals(resolve(url).func.view_class, RecipeIngredientAddView)

    def test_ingredient_edit_url_resolves(self):
        url = reverse("ingredients:ingredient-edit", args=[1, 1])
        self.assertEquals(resolve(url).func.view_class, RecipeIngredientEditView)

    def test_ingredient_delete_url_resolves(self):
        url = reverse("ingredients:ingredient-delete", args=[1, 1])
        self.assertEquals(resolve(url).func.view_class, RecipeIngredientDeleteView)
