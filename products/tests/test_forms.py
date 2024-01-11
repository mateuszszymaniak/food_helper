from django.test import TestCase

from ..forms import ProductForm


class ProductFormTest(TestCase):
    def test_valid_product_form(self):
        product_data = {"name": "test"}
        form = ProductForm(data=product_data)
        self.assertTrue(form.is_valid())

    def test_invalid_product_form(self):
        product_data = {"name": ""}
        form = ProductForm(data=product_data)
        self.assertFalse(form.is_valid())
