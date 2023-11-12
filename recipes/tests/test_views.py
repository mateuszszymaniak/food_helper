from http import HTTPStatus

from django.test import TestCase, tag
from django.urls import reverse

from users.factories import UserFactory
from users.models import Profile

from ..factories import RecipeFactory
from ..models import Ingredient, Recipe


class RecipesViews(TestCase):
    def setUp(self):
        self.recipes_home_page = reverse("recipes-home-page")
        self.recipe_add_page = reverse("recipe-add")
        self.user1 = UserFactory.create()
        self.profile1, _ = Profile.objects.get_or_create(user=self.user1)
        self.client.force_login(self.user1)
        self.recipe = RecipeFactory.create()
        self.recipe1 = Recipe.objects.create(
            recipe_name=self.recipe.recipe_name,
            preparation=self.recipe.preparation,
            user=self.profile1,
        )
        self.recipe_edit_page = reverse("recipe-edit", args=[self.recipe1.id])
        self.recipe_delete_page = reverse("recipe-delete", args=[self.recipe1.id])

    # region tests for home view
    def test_recipe_home_page_view_GET(self):
        Recipe.objects.all().delete()
        Ingredient.objects.all().delete()

        self.client.force_login(self.user1)
        response = self.client.get(self.recipes_home_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "recipes/home.html")
        self.assertContains(response, "Add recipe")

    # endregion
    # region tests for add view
    def test_recipe_add_page_view_GET(self):
        response = self.client.get(self.recipe_add_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "recipes/recipe_form.html")

    def test_recipe_add_page_view_POST_correct_data(self):
        Recipe.objects.all().delete()
        Ingredient.objects.all().delete()

        recipe = RecipeFactory.create()
        recipe_data = {
            "recipe_name": recipe.recipe_name,
            "preparation": recipe.preparation,
            "tags": [recipe.tags],
        }

        response = self.client.post(self.recipe_add_page, recipe_data, follow=True)

        self.assertEquals(Recipe.objects.count(), 1)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Recipe has been added")
        self.assertRedirects(response, expected_url=self.recipes_home_page)

    def test_recipe_add_page_view_POST_recipe_name_not_in_form(self):
        """
        recipe name is not inserted in form
        """
        recipe = RecipeFactory.create()
        recipe_data = {"preparation": recipe.preparation, "tags": [recipe.tags]}

        response = self.client.post(self.recipe_add_page, recipe_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Invalid data in recipe")
        self.assertRedirects(response, expected_url=self.recipe_add_page)

    def test_recipe_add_page_view_POST_preparation_not_in_form(self):
        """
        preparation is not inserted in form
        """
        recipe = RecipeFactory.create()
        recipe_data = {"recipe_name": recipe.recipe_name, "tags": [recipe.tags]}

        response = self.client.post(self.recipe_add_page, recipe_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Invalid data in recipe")
        self.assertRedirects(response, expected_url=self.recipe_add_page)

    # endregion
    # region tests for edit view
    def test_recipe_edit_page_view_GET(self):
        response = self.client.get(self.recipe_edit_page)
        self.assertContains(response, "Edit Recipe")
        self.assertContains(response, self.recipe1.recipe_name)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "recipes/recipe_form.html")

    def test_recipe_edit_page_view_POST_correct_data(self):
        recipe_data = {
            "recipe_name": "check_edit",
            "preparation": self.recipe.preparation,
        }

        response = self.client.post(self.recipe_edit_page, recipe_data, follow=True)
        self.assertEquals(
            Recipe.objects.get(id=self.recipe1.id).recipe_name, "check_edit"
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Recipe has been updated")
        self.assertRedirects(response, expected_url=self.recipes_home_page)

    # endregion
    # region tests for delete view
    def test_recipe_delete(self):
        self.client.post(self.recipe_delete_page)

        self.assertEquals(Recipe.objects.count(), 0)
        self.assertEquals(Ingredient.objects.count(), 0)

    # endregion
