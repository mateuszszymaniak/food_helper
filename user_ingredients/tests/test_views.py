from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from ingredients.models import Ingredient
from products.factorires import ProductFactory
from products.models import Product
from users.factories import UserFactory
from users.models import Profile

from ..factories import UserIngredientFactory
from ..models import UserIngredient


class UserIngredientsViews(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.client.force_login(self.user)
        self.product_factory = ProductFactory.create()
        self.user_ingredient_factory = UserIngredientFactory.create(user=self.profile)
        self.user_ingredients_home_page = reverse(
            "my_ingredients:useringredients-home-page"
        )
        self.user_ingredients_add_page = reverse("my_ingredients:useringredient-add")
        self.user_ingredients_add_page_with_product = reverse(
            "my_ingredients:useringredient-add", args=[self.product_factory.id]
        )
        self.user_ingredients_edit_page = reverse(
            "my_ingredients:useringredient-edit", args=[self.user_ingredient_factory.id]
        )
        self.user_ingredients_edit_page_with_product = reverse(
            "my_ingredients:useringredient-edit",
            args=[self.user_ingredient_factory.id, self.product_factory.id],
        )
        self.user_ingredients_delete_page = reverse(
            "my_ingredients:useringredient-delete",
            args=[self.user_ingredient_factory.id],
        )

    # region tests for home view
    def test_user_ingredients_home_page_view_without_ingredients_GET(self):
        UserIngredient.objects.all().delete()
        response = self.client.get(self.user_ingredients_home_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "useringredients/home.html")
        self.assertContains(response, "My Ingredients")
        self.assertContains(response, "Add")
        self.assertContains(response, "Add Ingredient")

    def test_user_ingredients_home_page_view_ingredients_GET(self):
        response = self.client.get(self.user_ingredients_home_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "useringredients/home.html")
        self.assertContains(response, "My Ingredients")
        self.assertContains(response, "Add")
        self.assertContains(
            response, self.user_ingredient_factory.ingredient.product.name
        )
        self.assertContains(
            response, self.user_ingredient_factory.ingredient.quantity_type
        )
        self.assertContains(response, self.user_ingredient_factory.amount)
        self.assertContains(
            response, f"my-ingredients/{self.user_ingredient_factory.id}/edit/"
        )
        self.assertContains(
            response, f"my-ingredients/{self.user_ingredient_factory.pk}/delete/"
        )

    # endregion
    # region tests for add view
    def test_user_ingredients_add_page_view_GET(self):
        response = self.client.get(self.user_ingredients_add_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "ingredients/ingredient_form.html")
        self.assertContains(response, "Add My Ingredient")
        self.assertContains(response, "Amount")
        self.assertNotContains(response, 'name="amount" value="')
        self.assertContains(response, "Quantity type")
        self.assertContains(response, 'value="" selected>---')
        self.assertContains(response, "Product name")
        self.assertContains(response, 'value="" selected>---')
        self.assertContains(response, "Add")
        self.assertContains(response, "Add Product")

    def test_user_ingredients_add_page_view_with_product_GET(self):
        response = self.client.get(self.user_ingredients_add_page_with_product)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "ingredients/ingredient_form.html")
        self.assertContains(response, "Add My Ingredient")
        self.assertContains(response, "Amount")
        self.assertNotContains(response, 'name="amount" value="')
        self.assertContains(response, "Quantity type")
        self.assertContains(response, 'value="" selected>---')
        self.assertContains(response, "Product name")
        self.assertContains(
            response,
            f'value="{self.product_factory.id}" selected>{self.product_factory.name}',
        )
        self.assertContains(response, "Add")
        self.assertContains(response, "Add Product")

    def test_user_ingredients_add_page_view_POST(self):
        user_ingredient_form = {
            "amount": "1",
            "ingredient-quantity_type": "kg",
            "ingredient-product_name": str(self.product_factory.id),
        }
        response = self.client.post(
            self.user_ingredients_add_page, user_ingredient_form, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.user_ingredients_home_page)
        self.assertContains(response, "My Ingredient has been successfully added")
        self.assertEquals(UserIngredient.objects.count(), 2)
        self.assertContains(response, self.product_factory.name)  # refresh_db test
        self.assertContains(
            response,
            f"my-ingredients/{UserIngredient.objects.get(ingredient=Ingredient.objects.get(product=Product.objects.get(name=self.product_factory.name), quantity_type='kg')).id}/edit/",
        )
        self.assertContains(
            response,
            f"my-ingredients/{UserIngredient.objects.get(ingredient=Ingredient.objects.get(product=Product.objects.get(name=self.product_factory.name), quantity_type='kg')).id}/delete/",
        )

    def test_user_ingredients_add_page_view_with_existing_ingredient_POST(self):
        user_ingredient_form = {
            "amount": "1",
            "ingredient-quantity_type": self.user_ingredient_factory.ingredient.quantity_type,
            "ingredient-product_name": str(
                self.user_ingredient_factory.ingredient.product.id
            ),
        }
        response = self.client.post(
            self.user_ingredients_add_page, user_ingredient_form, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.user_ingredients_home_page)
        self.assertContains(response, "has been added previously. Amount was updated")
        self.assertEquals(UserIngredient.objects.count(), 1)
        self.assertEquals(
            self.user_ingredient_factory.amount + 1,
            UserIngredient.objects.get(id=self.user_ingredient_factory.id).amount,
        )

    def test_user_ingredients_add_page_view_wrong_data_POST(self):
        user_ingredient_form = {
            "amount": "w",
            "ingredient-quantity_type": 1,
            "ingredient-product_name": "qw",
        }
        response = self.client.post(
            self.user_ingredients_add_page, user_ingredient_form, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.user_ingredients_add_page)
        self.assertContains(response, "Invalid data in my ingredients")

    # endregion
    # region tests for edit view
    def test_user_ingredients_edit_page_view_GET(self):
        response = self.client.get(self.user_ingredients_edit_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "ingredients/ingredient_form.html")
        self.assertContains(response, "Edit My Ingredient")
        self.assertContains(response, "Amount")
        self.assertContains(
            response, f'name="amount" value="{self.user_ingredient_factory.amount}"'
        )
        self.assertContains(response, "Quantity type")
        self.assertContains(
            response,
            f'value="{self.user_ingredient_factory.ingredient.quantity_type}" selected>',
        )
        self.assertContains(response, "Product name")
        self.assertContains(
            response,
            f'value="{self.user_ingredient_factory.ingredient.product.id}" selected>{self.user_ingredient_factory.ingredient.product.name}',
        )
        self.assertContains(response, "Save changes")

    def test_user_ingredients_edit_page_view_with_product_GET(self):
        response = self.client.get(self.user_ingredients_edit_page_with_product)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "ingredients/ingredient_form.html")
        self.assertContains(response, "Edit My Ingredient")
        self.assertContains(response, "Amount")
        self.assertContains(
            response, f'name="amount" value="{self.user_ingredient_factory.amount}"'
        )
        self.assertContains(response, "Quantity type")
        self.assertContains(
            response,
            f'value="{self.user_ingredient_factory.ingredient.quantity_type}" selected>',
        )
        self.assertContains(response, "Product name")
        self.assertContains(
            response,
            f'value="{self.product_factory.id}" selected>{self.product_factory.name}',
        )
        self.assertContains(response, "Save changes")

    def test_user_ingredients_edit_page_view_POST(self):
        new_product = ProductFactory.create()
        user_ingredient = {
            "amount": "10",
            "ingredient-quantity_type": "l",
            "ingredient-product_name": str(new_product.id),
        }
        response = self.client.post(
            self.user_ingredients_edit_page, user_ingredient, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.user_ingredients_home_page)
        self.assertContains(response, "Successfully edited my ingredient")
        self.assertEquals(UserIngredient.objects.count(), 1)
        self.assertContains(response, new_product.name)
        self.assertEquals(
            UserIngredient.objects.get(id=self.user_ingredient_factory.id).amount, 10
        )
        self.assertEquals(
            UserIngredient.objects.get(
                id=self.user_ingredient_factory.id
            ).ingredient.quantity_type,
            "l",
        )
        self.assertEquals(
            UserIngredient.objects.get(
                id=self.user_ingredient_factory.id
            ).ingredient.product.name,
            new_product.name,
        )

    def test_user_ingredients_edit_page_view_wrong_amount_POST(self):
        new_product = ProductFactory.create()
        user_ingredient = {
            "amount": "q",
            "ingredient-quantity_type": "l",
            "ingredient-product_name": str(new_product.id),
        }
        response = self.client.post(
            self.user_ingredients_edit_page, user_ingredient, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.user_ingredients_edit_page)
        self.assertContains(response, "Invalid data in editing my ingredient")
        self.assertContains(response, "Edit My Ingredient")
        self.assertContains(response, "Amount")
        self.assertContains(
            response, f'name="amount" value="{self.user_ingredient_factory.amount}"'
        )
        self.assertContains(response, "Quantity type")
        self.assertContains(
            response,
            f'value="{self.user_ingredient_factory.ingredient.quantity_type}" selected>',
        )
        self.assertContains(response, "Product name")
        self.assertContains(
            response,
            f'value="{self.user_ingredient_factory.ingredient.product.id}" selected>{self.user_ingredient_factory.ingredient.product.name}',
        )
        self.assertContains(response, "Save changes")

    def test_user_ingredients_edit_page_view_wrong_quantity_type_POST(self):
        new_product = ProductFactory.create()
        user_ingredient = {
            "amount": "5",
            "ingredient-quantity_type": "abc",
            "ingredient-product_name": str(new_product.id),
        }
        response = self.client.post(
            self.user_ingredients_edit_page, user_ingredient, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.user_ingredients_edit_page)
        self.assertContains(response, "Invalid data in editing my ingredient")
        self.assertContains(response, "Edit My Ingredient")
        self.assertContains(response, "Amount")
        self.assertContains(
            response, f'name="amount" value="{self.user_ingredient_factory.amount}"'
        )
        self.assertContains(response, "Quantity type")
        self.assertContains(
            response,
            f'value="{self.user_ingredient_factory.ingredient.quantity_type}" selected>',
        )
        self.assertContains(response, "Product name")
        self.assertContains(
            response,
            f'value="{self.user_ingredient_factory.ingredient.product.id}" selected>{self.user_ingredient_factory.ingredient.product.name}',
        )
        self.assertContains(response, "Save changes")

    def test_user_ingredients_edit_page_view_wrong_product_name_POST(self):
        user_ingredient = {
            "amount": "9",
            "ingredient-quantity_type": "l",
            "ingredient-product_name": "Kasza",
        }
        response = self.client.post(
            self.user_ingredients_edit_page, user_ingredient, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.user_ingredients_edit_page)
        self.assertContains(response, "Invalid data in editing my ingredient")
        self.assertContains(response, "Edit My Ingredient")
        self.assertContains(response, "Amount")
        self.assertContains(
            response, f'name="amount" value="{self.user_ingredient_factory.amount}"'
        )
        self.assertContains(response, "Quantity type")
        self.assertContains(
            response,
            f'value="{self.user_ingredient_factory.ingredient.quantity_type}" selected>',
        )
        self.assertContains(response, "Product name")
        self.assertContains(
            response,
            f'value="{self.user_ingredient_factory.ingredient.product.id}" selected>{self.user_ingredient_factory.ingredient.product.name}',
        )
        self.assertContains(response, "Save changes")

    # endregion
    # region tests for delete view
    def test_user_ingredient_delete(self):
        response = self.client.post(self.user_ingredients_delete_page, follow=True)
        self.assertContains(response, "Successfully removed my ingredient")
        self.assertEquals(UserIngredient.objects.count(), 0)
        self.assertNotEquals(
            response, self.user_ingredient_factory.ingredient.product.name
        )
