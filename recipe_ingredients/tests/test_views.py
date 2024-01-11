from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from ingredients.factories import IngredientFactory
from ingredients.models import Ingredient
from products.factorires import ProductFactory
from products.models import Product
from recipes.factories import RecipeFactory
from recipes.models import Recipe
from users.factories import UserFactory
from users.models import Profile

from ..factories import RecipeIngredientFactory
from ..models import RecipeIngredient


class RecipeIngredientsViews(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.client.force_login(self.user)
        self.product_factory = ProductFactory.create()
        self.ingredient_factory = IngredientFactory.create(product=self.product_factory)
        self.recipe_ingredient_factory = RecipeIngredientFactory.create(
            ingredient=self.ingredient_factory
        )
        self.recipe_factory = RecipeFactory.create(user=self.profile)
        Recipe.objects.get(id=self.recipe_factory.id).recipe_ingredient.add(
            self.recipe_ingredient_factory
        )
        self.recipe_ingredients_add_page = reverse(
            "recipe_ingredients:ingredient-add", args=[self.recipe_factory.id]
        )
        self.recipe_ingredients_add_page_with_product = reverse(
            "recipe_ingredients:ingredient-add",
            args=[self.recipe_factory.id, self.product_factory.id],
        )
        self.recipe_ingredients_edit_page = reverse(
            "recipe_ingredients:ingredient-edit",
            args=[self.recipe_factory.id, self.recipe_ingredient_factory.id],
        )
        self.recipe_ingredients_edit_page_with_product = reverse(
            "recipe_ingredients:ingredient-edit",
            args=[
                self.recipe_factory.id,
                self.recipe_ingredient_factory.id,
                self.product_factory.id,
            ],
        )
        self.recipe_ingredients_delete = reverse(
            "recipe_ingredients:ingredient-delete",
            args=[self.recipe_factory.id, self.recipe_ingredient_factory.id],
        )
        self.recipe_edit_page = reverse("recipe-edit", args=[self.recipe_factory.id])
        self.product_page = reverse("products:product-add")

    # region tests for add view
    def test_recipe_ingredients_add_page_view_GET(self):
        response = self.client.get(self.recipe_ingredients_add_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "ingredients/ingredient_form.html")
        self.assertContains(response, "Add Recipe Ingredient")
        self.assertContains(response, "Amount")
        self.assertNotContains(response, 'name="amount" value="')
        self.assertContains(response, "Quantity type")
        self.assertContains(response, 'value="" selected>---')
        self.assertContains(response, "Product name")
        self.assertContains(response, 'value="" selected>---')
        self.assertContains(response, "Add")
        self.assertContains(response, "Add Product")

    def test_recipe_ingredients_add_page_view_with_product_GET(self):
        response = self.client.get(self.recipe_ingredients_add_page_with_product)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "ingredients/ingredient_form.html")
        self.assertContains(response, "Add Recipe Ingredient")
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

    def test_recipe_ingredients_add_page_view_POST(self):
        recipe_ingredients_form = {
            "amount": "2",
            "ingredient-quantity_type": "szt.",
            "ingredient-product_name": str(self.product_factory.id),
        }
        response = self.client.post(
            self.recipe_ingredients_add_page, recipe_ingredients_form, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.recipe_edit_page)
        self.assertContains(response, "Successfully added ingredient")
        self.assertEquals(RecipeIngredient.objects.count(), 2)
        self.assertContains(response, "Edit Recipe")
        self.assertContains(response, "Ingredients")
        self.assertContains(response, "Add ingredient")
        self.assertContains(response, "Amount")
        self.assertContains(response, "2")
        self.assertContains(response, "Quantity type")
        self.assertContains(response, "szt.")
        self.assertContains(response, self.product_factory.name)
        self.assertContains(
            response,
            f"/recipe-ingredient/{self.recipe_factory.id}/edit-ingredient/{RecipeIngredient.objects.get(ingredient=Ingredient.objects.get(product=Product.objects.get(name=self.product_factory.name), quantity_type='szt.'), amount=2).id}/",
        )
        self.assertContains(
            response,
            f"/recipe-ingredient/{self.recipe_factory.id}/delete-ingredient/{RecipeIngredient.objects.get(ingredient=Ingredient.objects.get(product=Product.objects.get(name=self.product_factory.name), quantity_type='szt.'), amount=2).id}/",
        )

    def test_recipe_ingredients_add_page_view_invalid_form_POST(self):
        recipe_ingredient_form = {
            "amount": "q",
            "ingredient-quantity_type": "a",
            "ingredient-product_name": "Chleb",
        }
        response = self.client.post(
            self.recipe_ingredients_add_page, recipe_ingredient_form, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.recipe_ingredients_add_page)
        self.assertContains(response, "Invalid data in ingredient")
        self.assertContains(response, "Add Recipe Ingredient")
        self.assertContains(response, "Amount")
        self.assertNotContains(response, 'name="amount" value="')
        self.assertContains(response, "Quantity type")
        self.assertContains(response, 'value="" selected>---')
        self.assertContains(response, "Product name")
        self.assertContains(response, 'value="" selected>---')
        self.assertContains(response, "Add")
        self.assertContains(response, "Add Product")

    # endregion
    # region tests for edit view
    def test_recipe_ingredients_edit_page_view_GET(self):
        response = self.client.get(self.recipe_ingredients_edit_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "ingredients/ingredient_form.html")
        self.assertContains(response, "Edit Recipe Ingredient")
        self.assertContains(response, "Amount")
        self.assertContains(
            response, f'name="amount" value="{self.recipe_ingredient_factory.amount}"'
        )
        self.assertContains(response, "Quantity type")
        self.assertContains(
            response,
            f'value="{self.recipe_ingredient_factory.ingredient.quantity_type}" selected>',
        )
        self.assertContains(response, "Product name")
        self.assertContains(
            response,
            f'value="{self.recipe_ingredient_factory.ingredient.product.id}" selected>{self.recipe_ingredient_factory.ingredient.product.name}',
        )
        self.assertContains(response, "Save changes")

    def test_recipe_ingredients_edit_page_view_with_product_GET(self):
        response = self.client.get(self.recipe_ingredients_edit_page_with_product)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "ingredients/ingredient_form.html")
        self.assertContains(response, "Edit Recipe Ingredient")
        self.assertContains(response, "Amount")
        self.assertContains(
            response, f'name="amount" value="{self.recipe_ingredient_factory.amount}"'
        )
        self.assertContains(response, "Quantity type")
        self.assertContains(
            response,
            f'value="{self.recipe_ingredient_factory.ingredient.quantity_type}" selected>',
        )
        self.assertContains(response, "Product name")
        self.assertContains(
            response,
            f'value="{self.recipe_ingredient_factory.ingredient.product.id}" selected>{self.recipe_ingredient_factory.ingredient.product.name}',
        )
        self.assertContains(response, "Save changes")

    def test_recipe_ingredients_edit_page_view_POST(self):
        new_product = ProductFactory.create()
        recipe_ingredient_form = {
            "amount": "10",
            "ingredient-quantity_type": "l",
            "ingredient-product_name": str(new_product.id),
        }
        response = self.client.post(
            self.recipe_ingredients_edit_page, recipe_ingredient_form, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.recipe_edit_page)
        self.assertContains(response, "Successfully edited ingredient")
        self.assertEquals(RecipeIngredient.objects.count(), 1)
        self.assertContains(response, new_product.name)
        self.recipe_ingredient_factory.refresh_from_db()  # działa -> zaktualizowac testy
        self.assertEquals(self.recipe_ingredient_factory.amount, 10)
        self.assertEquals(self.recipe_ingredient_factory.ingredient.quantity_type, "l")
        self.assertEquals(
            self.recipe_ingredient_factory.ingredient.product.name, new_product.name
        )

    def test_recipe_ingredients_edit_page_view_wrong_amount_POST(self):
        new_product = ProductFactory.create()
        recipe_ingredient_form = {
            "amount": "a",
            "ingredient-quantity_type": "kg",
            "ingredient-product_name": str(new_product.id),
        }
        response = self.client.post(
            self.recipe_ingredients_edit_page, recipe_ingredient_form, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.recipe_ingredients_edit_page)
        self.assertContains(response, "Invalid data in ingredient")
        self.assertContains(response, "Edit Recipe Ingredient")
        self.assertContains(response, "Amount")
        self.assertContains(
            response, f'name="amount" value="{self.recipe_ingredient_factory.amount}"'
        )
        self.assertContains(response, "Quantity type")
        self.assertContains(
            response,
            f'value="{self.recipe_ingredient_factory.ingredient.quantity_type}" selected>',
        )
        self.assertContains(response, "Product name")
        self.assertContains(
            response,
            f'value="{self.recipe_ingredient_factory.ingredient.product.id}" selected>{self.recipe_ingredient_factory.ingredient.product.name}',
        )
        self.assertContains(response, "Save changes")

    def test_recipe_ingredients_edit_page_view_wrong_quantity_type_POST(self):
        new_product = ProductFactory.create()
        recipe_ingredient_form = {
            "amount": "5",
            "ingredient-quantity_type": "abc",
            "ingredient-product_name": str(new_product.id),
        }
        response = self.client.post(
            self.recipe_ingredients_edit_page, recipe_ingredient_form, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.recipe_ingredients_edit_page)
        self.assertContains(response, "Invalid data in ingredient")
        self.assertContains(response, "Edit Recipe Ingredient")
        self.assertContains(response, "Amount")
        self.assertContains(
            response, f'name="amount" value="{self.recipe_ingredient_factory.amount}"'
        )
        self.assertContains(response, "Quantity type")
        self.assertContains(
            response,
            f'value="{self.recipe_ingredient_factory.ingredient.quantity_type}" selected>',
        )
        self.assertContains(response, "Product name")
        self.assertContains(
            response,
            f'value="{self.recipe_ingredient_factory.ingredient.product.id}" selected>{self.recipe_ingredient_factory.ingredient.product.name}',
        )
        self.assertContains(response, "Save changes")

    def test_recipe_ingredients_edit_page_view_wrong_product_name_POST(self):
        recipe_ingredient_form = {
            "amount": "1",
            "ingredient-quantity_type": "kg",
            "ingredient-product_name": "xyz",
        }
        response = self.client.post(
            self.recipe_ingredients_edit_page, recipe_ingredient_form, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.recipe_ingredients_edit_page)
        self.assertContains(response, "Invalid data in ingredient")
        self.assertContains(response, "Edit Recipe Ingredient")
        self.assertContains(response, "Amount")
        self.assertContains(
            response, f'name="amount" value="{self.recipe_ingredient_factory.amount}"'
        )
        self.assertContains(response, "Quantity type")
        self.assertContains(
            response,
            f'value="{self.recipe_ingredient_factory.ingredient.quantity_type}" selected>',
        )
        self.assertContains(response, "Product name")
        self.assertContains(
            response,
            f'value="{self.recipe_ingredient_factory.ingredient.product.id}" selected>{self.recipe_ingredient_factory.ingredient.product.name}',
        )
        self.assertContains(response, "Save changes")

    # endregion
    # region tests for delete view
    def test_recipe_ingresient_delete(self):
        response = self.client.post(self.recipe_ingredients_delete, follow=True)
        self.assertContains(response, "Successfully removed ingredient")
        self.assertEquals(RecipeIngredient.objects.count(), 0)
        self.assertNotEquals(
            response, self.recipe_ingredient_factory.ingredient.product.name
        )

    # endregion
