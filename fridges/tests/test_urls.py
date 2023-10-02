from django.test import SimpleTestCase
from django.urls import resolve, reverse

from fridges.views import (
    FridgeAddPageView,
    FridgesHomePageView,
    IngredientDeleteView,
    IngredientEditPageView,
)


class TestUrls(SimpleTestCase):
    def test_fridges_home_page_url_resolves(self):
        url = reverse("fridges-home-page")
        self.assertEqual(resolve(url).func.view_class, FridgesHomePageView)

    def test_fridges_add_url_resolves(self):
        url = reverse("fridge-add")
        self.assertEqual(resolve(url).func.view_class, FridgeAddPageView)

    def test_fridge_edit_url_resolves(self):
        url = reverse("fridge-edit", args=[1])
        self.assertEqual(resolve(url).func.view_class, IngredientEditPageView)

    def test_fridge_delete_url_resolves(self):
        url = reverse("fridge-delete", args=[2])
        self.assertEqual(resolve(url).func.view_class, IngredientDeleteView)
