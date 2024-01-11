from django.test import SimpleTestCase
from django.urls import resolve, reverse

from ..views import (
    ProductAddPageView,
    ProductDeleteView,
    ProductEditPageView,
    ProductHomePageView,
)


class TestUrls(SimpleTestCase):
    def test_product_home_page_url_resolves(self):
        url = reverse("products:products-home-page")
        self.assertEquals(resolve(url).func.view_class, ProductHomePageView)

    def test_product_add_url_resolves(self):
        url = reverse("products:product-add")
        self.assertEquals(resolve(url).func.view_class, ProductAddPageView)

    def test_product_edit_url_resolves(self):
        url = reverse("products:product-edit", args=[12])
        self.assertEquals(resolve(url).func.view_class, ProductEditPageView)

    def test_product_delete_url_resolves(self):
        url = reverse("products:product-delete", args=[1])
        self.assertEquals(resolve(url).func.view_class, ProductDeleteView)
