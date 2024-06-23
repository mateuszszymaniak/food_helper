from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from ingredients.models import Ingredient
from recipe_ingredients.factories import RecipeIngredientFactory
from users.factories import UserFactory
from users.models import Profile

from ..factories import RecipeFactory
from ..models import Recipe


class RecipesViews(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.client.force_login(self.user)
        self.recipe_ingredient_factory = RecipeIngredientFactory.create()
        self.recipe = RecipeFactory.create(user=self.profile)
        Recipe.objects.get(id=self.recipe.id).recipe_ingredient.add(
            self.recipe_ingredient_factory
        )
        self.recipes_home_page = reverse("recipes-home-page")
        self.recipe_add_page = reverse("recipe-add")
        self.recipe_edit_page = reverse("recipe-edit", args=[self.recipe.id])
        self.recipe_delete_page = reverse("recipe-delete", args=[self.recipe.id])
        self.recipe_ingredient_page = reverse(
            "recipe_ingredients:ingredient-add", args=[self.recipe.id]
        )

    # region tests for home view
    def test_recipe_home_page_view_without_recipes_GET(self):
        Recipe.objects.all().delete()
        Ingredient.objects.all().delete()

        response = self.client.get(self.recipes_home_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "recipes/home.html")
        self.assertContains(response, "Recipes")
        self.assertContains(response, "Add")
        self.assertContains(response, "Add recipe")

    def test_recipe_home_page_view_GET(self):
        response = self.client.get(self.recipes_home_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "recipes/home.html")
        self.assertContains(response, "Recipes")
        self.assertContains(response, "Add")
        self.assertContains(response, "Recipe name")
        self.assertContains(response, self.recipe.recipe_name)
        self.assertContains(response, "Ingredients")
        self.assertContains(
            response,
            f"{self.recipe_ingredient_factory.amount} {self.recipe_ingredient_factory.ingredient.quantity_type} {self.recipe_ingredient_factory.ingredient.product.name}",
        )
        self.assertContains(response, "Preparation")
        self.assertContains(response, self.recipe.preparation)
        # self.assertContains(response, "Tags")
        # self.assertContains(response, self.recipe.tags[0])
        self.assertContains(response, f"recipes/{self.recipe.id}/edit")
        self.assertContains(response, f"recipes/{self.recipe.id}/delete")

    # endregion
    # region tests for add view
    def test_recipe_add_page_view_GET(self):
        response = self.client.get(self.recipe_add_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "recipes/recipe_form_new.html")
        self.assertContains(response, "Add Recipe")
        self.assertContains(response, "Recipe name")
        self.assertContains(response, '<input type="text" name="recipe_name"')
        self.assertContains(response, "Ingredients")
        self.assertContains(response, "Add ingredient")
        self.assertContains(response, "Preparation")
        self.assertContains(response, '<textarea name="preparation"')
        # self.assertContains(response, "Tags")
        # self.assertContains(response, '<input type="text" name="tags"')
        self.assertContains(response, "Add")

    def test_recipe_add_page_view_POST(self):
        recipe_form = {
            "recipe_name": "new recipe",
            "preparation": "xyz",
            # "tags": "dish",
        }
        response = self.client.post(self.recipe_add_page, recipe_form, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.recipes_home_page)
        self.assertContains(response, "Recipe has been added")
        self.assertEquals(Recipe.objects.count(), 2)
        self.assertContains(response, "new recipe")
        self.assertContains(
            response, f"recipes/{Recipe.objects.get(recipe_name='new recipe').id}/edit"
        )
        self.assertContains(
            response,
            f"recipes/{Recipe.objects.get(recipe_name='new recipe').id}/delete",
        )

    def test_recipe_add_page_view_without_recipe_name_POST(self):
        recipe_form = {}
        response = self.client.post(self.recipe_add_page, recipe_form, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.recipe_add_page)
        self.assertContains(response, "Invalid data in recipe")
        self.assertEquals(Recipe.objects.count(), 1)

    def test_redirect_to_add_ingredient_from_add_recipe_POST(self):
        recipe_form = {
            "recipe_name": "q",
            "add_ingredient": "add_ingredient",
        }
        response = self.client.post(self.recipe_add_page, recipe_form, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(
            response,
            expected_url="/recipe-ingredient/"
            + str(Recipe.objects.get(recipe_name="q").id)
            + "/add-ingredient/",
        )

    # endregion
    # region tests for edit view
    def test_recipe_edit_page_view_GET(self):
        response = self.client.get(self.recipe_edit_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "recipes/recipe_form_edit.html")
        self.assertContains(response, "Edit Recipe")
        self.assertContains(response, "Recipe name")
        self.assertContains(response, self.recipe.recipe_name)
        self.assertContains(response, "Ingredients")
        self.assertContains(response, "Add ingredient")
        self.assertContains(response, "Amount")
        self.assertContains(response, "Quantity type")
        self.assertContains(response, "Product")
        self.assertContains(response, self.recipe_ingredient_factory.amount)
        self.assertContains(
            response, self.recipe_ingredient_factory.ingredient.quantity_type
        )
        self.assertContains(
            response, self.recipe_ingredient_factory.ingredient.product.name
        )
        self.assertContains(
            response, self.recipe_ingredient_factory.ingredient.product.name
        )
        self.assertContains(
            response,
            f"recipe-ingredient/{self.recipe.id}/edit-ingredient/{self.recipe_ingredient_factory.id}",
        )
        self.assertContains(
            response,
            f"recipe-ingredient/{self.recipe.id}/delete-ingredient/{self.recipe_ingredient_factory.id}",
        )
        self.assertContains(response, "Preparation")
        self.assertContains(response, self.recipe.preparation)
        # self.assertContains(response, "Tags")
        # self.assertContains(response, self.recipe.tags[0])
        self.assertContains(response, "Save changes")

    def test_recipe_edit_page_view_POST(self):
        recipe_form = {
            "recipe_name": "qwerty",
            "preparation": "zxc",
            # "tags": "abc",
        }
        response = self.client.post(self.recipe_edit_page, recipe_form, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.recipes_home_page)
        self.assertContains(response, "Recipe has been updated")
        self.assertEquals(Recipe.objects.count(), 1)
        self.assertContains(response, "qwerty")
        self.assertEquals(Recipe.objects.get(id=self.recipe.id).recipe_name, "qwerty")
        self.assertEquals(Recipe.objects.get(id=self.recipe.id).preparation, "zxc")
        # self.assertEquals(Recipe.objects.get(id=self.recipe.id).tags[0], "abc")

    def test_recipe_edit_page_view_wrong_data_POST(self):
        recipe_form = {}
        response = self.client.post(self.recipe_edit_page, recipe_form, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.recipe_edit_page)
        self.assertContains(response, "Invalid data in recipe")
        self.assertContains(response, "Edit Recipe")
        self.assertContains(response, "Recipe name")
        self.assertContains(response, self.recipe.recipe_name)
        self.assertContains(response, "Ingredients")
        self.assertContains(response, "Add ingredient")
        self.assertContains(response, "Amount")
        self.assertContains(response, "Quantity type")
        self.assertContains(response, "Product")
        self.assertContains(response, self.recipe_ingredient_factory.amount)
        self.assertContains(
            response, self.recipe_ingredient_factory.ingredient.quantity_type
        )
        self.assertContains(
            response, self.recipe_ingredient_factory.ingredient.product.name
        )
        self.assertContains(
            response, self.recipe_ingredient_factory.ingredient.product.name
        )
        self.assertContains(
            response,
            f"recipe-ingredient/{self.recipe.id}/edit-ingredient/{self.recipe_ingredient_factory.id}",
        )
        self.assertContains(
            response,
            f"recipe-ingredient/{self.recipe.id}/delete-ingredient/{self.recipe_ingredient_factory.id}",
        )
        self.assertContains(response, "Preparation")
        self.assertContains(response, self.recipe.preparation)
        # self.assertContains(response, "Tags")
        # self.assertContains(response, self.recipe.tags[0])
        self.assertContains(response, "Save changes")

    def test_redirect_to_add_ingredient_from_edit_recipe_POST(self):
        recipe_form = {
            "recipe_name": "q",
            "add_ingredient": "add_ingredient",
        }
        response = self.client.post(self.recipe_edit_page, recipe_form, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.recipe_ingredient_page)

    # endregion
    # region tests for delete view
    def test_recipe_delete(self):
        response = self.client.post(self.recipe_delete_page, follow=True)
        self.assertContains(response, "Successfully remove recipe")
        self.assertEquals(Recipe.objects.count(), 0)
        self.assertNotEquals(response, self.recipe.recipe_name)

    # endregion
