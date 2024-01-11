from django.test import SimpleTestCase
from django.urls import resolve, reverse

from ..views import (
    UserIngredientsAddPageView,
    UserIngredientsDeletePageView,
    UserIngredientsEditPageView,
    UserIngredientsHomePageView,
)


class TestUrls(SimpleTestCase):
    def test_user_ingredients_home_page_url_resolves(self):
        url = reverse("my_ingredients:useringredients-home-page")
        self.assertEquals(resolve(url).func.view_class, UserIngredientsHomePageView)

    def test_user_ingredients_add_url_resolves(self):
        url = reverse("my_ingredients:useringredient-add")
        self.assertEquals(resolve(url).func.view_class, UserIngredientsAddPageView)

    def test_user_ingredients_add_url_with_product_id_resolves(self):
        url = reverse("my_ingredients:useringredient-add", args=[11])
        self.assertEquals(resolve(url).func.view_class, UserIngredientsAddPageView)

    def test_user_ingredients_edit_url_resolves(self):
        url = reverse("my_ingredients:useringredient-edit", args=[3])
        self.assertEquals(resolve(url).func.view_class, UserIngredientsEditPageView)

    def test_user_ingredients_edit_url_with_product_id_resolves(self):
        url = reverse("my_ingredients:useringredient-edit", args=[1, 7])
        self.assertEquals(resolve(url).func.view_class, UserIngredientsEditPageView)

    def test_user_ingredients_delete_url_resolves(self):
        url = reverse("my_ingredients:useringredient-delete", args=[2])
        self.assertEquals(resolve(url).func.view_class, UserIngredientsDeletePageView)
