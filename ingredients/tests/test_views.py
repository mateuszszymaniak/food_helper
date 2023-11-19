from http import HTTPStatus

from django.test import TestCase, tag
from django.urls import reverse

from recipes.factories import RecipeFactory
from recipes.models import Recipe
from users.factories import UserFactory
from users.models import Profile

from ..factories import IngredientFactory
from ..models import Ingredient


class IngredientsViews(TestCase):
    def setUp(self):
        self.user1 = UserFactory.create()
        self.profile1, _ = Profile.objects.get_or_create(user=self.user1)
        self.client.force_login(self.user1)
        self.ingredient_factory = IngredientFactory.create()
        self.ingredient = Ingredient.objects.create(
            name=self.ingredient_factory.name,
            quantity=self.ingredient_factory.quantity,
            quantity_type=self.ingredient_factory.quantity_type,
        )
        self.recipe_factory = RecipeFactory.create()
        self.recipe = Recipe.objects.create(
            recipe_name=self.recipe_factory.recipe_name,
            preparation=self.recipe_factory.preparation,
            user=self.profile1,
        )
        self.recipe.ingredients.add(self.ingredient)
        self.ingredient_add_page = reverse(
            "ingredients:ingredient-add", args=[self.recipe.id]
        )
        self.ingredient_edit_page = reverse(
            "ingredients:ingredient-edit", args=[self.recipe.id, self.ingredient.id]
        )
        self.ingredient_delete_page = reverse(
            "ingredients:ingredient-delete", args=[self.recipe.id, self.ingredient.id]
        )
        self.recipe_edit_page = reverse("recipe-edit", args=[self.recipe.id])

    # region tests for add view
    def test_ingredient_add_page_view_GET(self):
        response = self.client.get(self.ingredient_add_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "ingredients/ingredient_form.html")

    def test_ingredient_add_page_view_POST_correct_data(self):
        ingredient = IngredientFactory.create()
        ingredient_data = {
            "name": ingredient.name,
            "quantity": ingredient.quantity,
            "quantity_type": ingredient.quantity_type,
        }
        response = self.client.post(
            self.ingredient_add_page, ingredient_data, follow=True
        )

        self.assertEquals(Ingredient.objects.count(), 2)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Successfully added ingredient")
        self.assertRedirects(response, expected_url=self.recipe_edit_page)

    def test_ingredient_add_page_view_POST_missing_ingredient_name(self):
        ingredient = IngredientFactory.create()
        ingredient_data = {
            "quantity": ingredient.quantity,
            "quantity_type": ingredient.quantity_type,
        }
        response = self.client.post(
            self.ingredient_add_page, ingredient_data, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Invalid data in ingredient")
        self.assertRedirects(response, expected_url=self.ingredient_add_page)

    def test_ingredient_add_page_view_POST_missing_ingredient_quantity(self):
        ingredient = IngredientFactory.create()
        ingredient_data = {
            "name": ingredient.name,
            "quantity_type": ingredient.quantity_type,
        }
        response = self.client.post(
            self.ingredient_add_page, ingredient_data, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Invalid data in ingredient")
        self.assertRedirects(response, expected_url=self.ingredient_add_page)

    def test_ingredient_add_page_view_POST_missing_ingredient_quantity_type(self):
        ingredient = IngredientFactory.create()
        ingredient_data = {
            "name": ingredient.name,
            "quantity": ingredient.quantity,
        }
        response = self.client.post(
            self.ingredient_add_page, ingredient_data, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Invalid data in ingredient")
        self.assertRedirects(response, expected_url=self.ingredient_add_page)

    # endregion
    # region tests for edit view
    def test_ingredient_edit_page_view_GET(self):
        response = self.client.get(self.ingredient_edit_page)
        self.assertContains(response, self.ingredient.name)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "ingredients/ingredient_form.html")

    def test_ingredient_edit_page_view_POST_correct_data(self):
        ingredient_data = {
            "name": "new_name",
            "quantity": self.ingredient.quantity,
            "quantity_type": self.ingredient.quantity_type,
        }

        response = self.client.post(
            self.ingredient_edit_page, ingredient_data, follow=True
        )
        self.assertEquals(
            Ingredient.objects.get(id=self.ingredient.id).name, "new_name"
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Successfully edited ingredient")
        self.assertRedirects(response, expected_url=self.recipe_edit_page)

    def test_ingredient_edit_page_view_POST_incorrect_data(self):
        ingredient_data = {
            "name": "new_name",
        }

        response = self.client.post(
            self.ingredient_edit_page, ingredient_data, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Invalid data in ingredient")
        self.assertRedirects(response, expected_url=self.ingredient_edit_page)

    # endregion
    # region tests for delete view
    def test_ingredient_delete(self):
        response = self.client.post(self.ingredient_delete_page, follow=True)

        self.assertEquals(Ingredient.objects.count(), 0)
        self.assertContains(response, "Successfully removed ingredient")

    # endregion
