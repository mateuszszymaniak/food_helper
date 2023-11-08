from django.test import SimpleTestCase, tag
from django.urls import resolve, reverse

from ingredients.views import (
    IngredientAddView,
    IngredientDeleteView,
    IngredientEditView,
)


class TestUrls(SimpleTestCase):
    def test_ingredient_add_url_resolves(self):
        url = reverse("ingredients:ingredient-add", args=[1])
        self.assertEquals(resolve(url).func.view_class, IngredientAddView)

    def test_ingredient_edit_url_resolves(self):
        url = reverse("ingredients:ingredient-edit", args=[1, 1])
        self.assertEquals(resolve(url).func.view_class, IngredientEditView)

    def test_ingredient_delete_url_resolves(self):
        url = reverse("ingredients:ingredient-delete", args=[1, 1])
        self.assertEquals(resolve(url).func.view_class, IngredientDeleteView)
