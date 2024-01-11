from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.factories import UserFactory
from users.models import Profile

from ..factorires import ProductFactory
from ..models import Product


class ProductsViews(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.client.force_login(self.user)
        self.product_factory1 = ProductFactory.create()
        self.products_home_page = reverse("products:products-home-page")
        self.product_add_page = reverse("products:product-add")
        self.product_add_page_referer = reverse("products:product-add")
        self.product_edit_page = reverse(
            "products:product-edit", args=[self.product_factory1.id]
        )
        self.product_delete_page = reverse(
            "products:product-delete", args=[self.product_factory1.id]
        )

    # region tests for home view
    def test_products_home_page_view_without_products_GET(self):
        Product.objects.all().delete()
        response = self.client.get(self.products_home_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/home.html")
        self.assertContains(response, "Products")
        self.assertContains(response, "Add")
        self.assertContains(response, "Add Product")

    def test_products_home_page_view_with_products_GET(self):
        response = self.client.get(self.products_home_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/home.html")
        self.assertContains(response, "Products")
        self.assertContains(response, "Add")
        self.assertContains(response, self.product_factory1.name)
        self.assertContains(response, f"product/{self.product_factory1.id}/edit/")
        self.assertContains(response, f"product/{self.product_factory1.id}/delete/")

    # endregion
    # region tests for add view
    def test_product_add_page_view_GET(self):
        response = self.client.get(self.product_add_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/product_form.html")
        self.assertContains(response, "Add Product")
        self.assertContains(response, "Name")
        self.assertNotContains(response, 'name="name" value="')
        self.assertContains(response, "Add")

    def test_product_add_page_view_POST_new_product(self):
        product_form = {"name": "new_product"}
        response = self.client.post(self.product_add_page, product_form, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.products_home_page)
        self.assertContains(response, "Product has been added")
        self.assertEquals(Product.objects.count(), 2)
        self.assertContains(response, "new_product")
        self.assertContains(
            response, f"product/{Product.objects.get(name='new_product').id}/edit/"
        )
        self.assertContains(
            response, f"product/{Product.objects.get(name='new_product').id}/delete/"
        )

    def test_product_add_page_view_redirect_to_http_referer_POST(self):
        self.client.get(
            self.product_add_page_referer, {}, HTTP_REFERER="/my-ingredients/add/"
        )
        product_form = {"name": "prod"}
        response = self.client.post(self.product_add_page, product_form, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Add My Ingredient")

    def test_product_add_page_view_POST_existing_product(self):
        product_form = {"name": self.product_factory1.name}
        response = self.client.post(self.product_add_page, product_form, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.product_add_page)
        self.assertContains(response, "Invalid data in product")
        self.assertEquals(Product.objects.count(), 1)

    # endregion
    # region tests for edit view
    def test_product_edit_page_view_GET(self):
        response = self.client.get(self.product_edit_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/product_form.html")
        self.assertContains(response, "Edit Product")
        self.assertContains(response, self.product_factory1.name)
        self.assertContains(response, "Save changes")

    def test_product_edit_page_view_POST_edited_product(self):
        product_form = {"name": "new_product"}
        response = self.client.post(self.product_edit_page, product_form, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.products_home_page)
        self.assertContains(response, "Successfully edited product")
        self.assertEquals(Product.objects.count(), 1)
        self.assertContains(response, "new_product")
        self.assertEquals(
            Product.objects.get(id=self.product_factory1.id).name, "new_product"
        )

    def test_product_edit_page_view_POST_existing_product(self):
        product_form = {"name": self.product_factory1.name}
        response = self.client.post(self.product_edit_page, product_form, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.product_edit_page)
        self.assertContains(response, "Invalid data in product")
        self.assertEquals(
            Product.objects.get(id=self.product_factory1.id).name,
            self.product_factory1.name,
        )

    # endregion
    # region tests for delete view
    def test_product_delete(self):
        response = self.client.post(self.product_delete_page, follow=True)
        self.assertContains(response, "Successfully removed product")
        self.assertEquals(Product.objects.count(), 0)
        self.assertNotEquals(response, self.product_factory1.name)

    # endregion
