from django.test import SimpleTestCase
from django.urls import resolve, reverse

from ..views import (
    RecipeIngredientAddView,
    RecipeIngredientDeleteView,
    RecipeIngredientEditView,
)


class TestUrls(SimpleTestCase):
    def test_recipe_ingredients_add_url_resolves(self):
        url = reverse("recipe_ingredients:ingredient-add", args=[11])
        self.assertEquals(resolve(url).func.view_class, RecipeIngredientAddView)

    def test_recipe_ingredients_add_url_with_product_id_resolves(self):
        url = reverse("recipe_ingredients:ingredient-add", args=[9, 1])
        self.assertEquals(resolve(url).func.view_class, RecipeIngredientAddView)

    def test_recipe_ingredients_edit_url_resolves(self):
        url = reverse("recipe_ingredients:ingredient-edit", args=[8, 5])
        self.assertEquals(resolve(url).func.view_class, RecipeIngredientEditView)

    def test_recipe_ingredients_edit_url_with_product_id_resolves(self):
        url = reverse("recipe_ingredients:ingredient-edit", args=[7, 6, 11])
        self.assertEquals(resolve(url).func.view_class, RecipeIngredientEditView)

    def test_recipe_ingredients_delete_url_resolves(self):
        url = reverse("recipe_ingredients:ingredient-delete", args=[8, 2])
        self.assertEquals(resolve(url).func.view_class, RecipeIngredientDeleteView)
