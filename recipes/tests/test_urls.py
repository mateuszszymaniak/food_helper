from django.test import SimpleTestCase
from django.urls import resolve, reverse

from recipes.views import (
    RecipeAddPageView,
    RecipeDeleteView,
    RecipeEditPageView,
    RecipesHomePageView,
)


class TestUrls(SimpleTestCase):
    def test_recipes_home_page_url_resolves(self):
        url = reverse("recipes-home-page")
        self.assertEqual(resolve(url).func.view_class, RecipesHomePageView)

    def test_recipe_add_url_resolves(self):
        url = reverse("recipe-add")
        self.assertEquals(resolve(url).func.view_class, RecipeAddPageView)

    def test_recipe_edit_url_resolves(self):
        url = reverse("recipe-edit", args=[1])
        self.assertEquals(resolve(url).func.view_class, RecipeEditPageView)

    def test_recipe_delete_url_resolves(self):
        url = reverse("recipe-delete", args=[2])
        self.assertEquals(resolve(url).func.view_class, RecipeDeleteView)
