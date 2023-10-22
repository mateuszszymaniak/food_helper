from http import HTTPStatus

from django.test import TestCase, tag
from django.urls import reverse

from users.models import Profile, User

from ..factories import IngredientFactory, RecipeFactory
from ..models import Ingredient, Recipe


class RecipesViews(TestCase):
    def setUp(self):
        self.recipes_home_page = reverse("recipes-home-page")
        self.recipe_add_page = reverse("recipe-add")
        self.user_username = "user1"
        self.user_password = "pass1!"  # nosec bandit B105
        self.user_email = "email@email.pl"
        self.user1 = User.objects.create(
            username=self.user_username,
            email=self.user_email,
        )
        self.user1.set_password(self.user_password)
        self.user1.save()
        self.profile1, _ = Profile.objects.get_or_create(user=self.user1)
        self.client.force_login(self.user1)
        self.recipe1 = Recipe.objects.create(
            recipe_name="rec1", preparation="123\nqwe", user=self.profile1
        )
        self.ingredient1 = Ingredient.objects.get_or_create(
            name="ing1", quantity="1", quantity_type="l"
        )
        self.recipe1.ingredients.add(self.ingredient1[0].id)
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

        ingredient = IngredientFactory.create()
        recipe_data["name-0"] = ingredient.name
        recipe_data["quantity-0"] = str(ingredient.quantity)
        recipe_data["quantity_type-0"] = ingredient.quantity_type

        response = self.client.post(self.recipe_add_page, recipe_data, follow=True)

        self.assertEquals(Recipe.objects.count(), 1)
        self.assertEquals(Ingredient.objects.count(), 1)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Przepis został dodany")
        self.assertRedirects(response, expected_url=self.recipes_home_page)

    def test_recipe_add_page_view_POST_ingredients_not_in_form(self):
        """
        ingredients are not added in form
        """
        recipe = RecipeFactory.create()
        recipe_data = {
            "recipe_name": recipe.recipe_name,
            "preparation": recipe.preparation,
            "tags": [recipe.tags],
        }
        response = self.client.post(self.recipe_add_page, recipe_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Invalid data in recipe")
        self.assertRedirects(response, expected_url=self.recipe_add_page)

    def test_recipe_add_page_view_POST_recipe_name_not_in_form(self):
        """
        recipe name is not inserted in form
        """
        recipe = RecipeFactory.create()
        ingredient = IngredientFactory.create()
        recipe_data = {"preparation": recipe.preparation, "tags": [recipe.tags]}

        recipe_data["name-0"] = ingredient.name
        recipe_data["quantity-0"] = ingredient.quantity
        recipe_data["quantity_type-0"] = ingredient.quantity_type
        response = self.client.post(self.recipe_add_page, recipe_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Invalid data in recipe")
        self.assertRedirects(response, expected_url=self.recipe_add_page)

    def test_recipe_add_page_view_POST_preparation_not_in_form(self):
        """
        preparation is not inserted in form
        """
        recipe = RecipeFactory.create()
        ingredient = IngredientFactory.create()
        recipe_data = {"recipe_name": recipe.recipe_name, "tags": [recipe.tags]}

        recipe_data["name-0"] = ingredient.name
        recipe_data["quantity-0"] = ingredient.quantity
        recipe_data["quantity_type-0"] = ingredient.quantity_type
        response = self.client.post(self.recipe_add_page, recipe_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Invalid data in recipe")
        self.assertRedirects(response, expected_url=self.recipe_add_page)

    # endregion
    # region tests for edit view
    def test_recipe_edit_page_view_GET(self):
        response = self.client.get(self.recipe_edit_page)
        self.assertContains(response, "Edytuj przepis!")
        self.assertContains(response, self.recipe1.recipe_name)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "recipes/recipe_form.html")

        # TODO dopisać POSTa

    # endregion
    # region tests for delete view
    def test_recipe_delete(self):
        initial_recipe = Recipe.objects.count()
        initial_ingredients = Ingredient.objects.count()
        response = self.client.post(self.recipe_delete_page)
        finish_recipe = Recipe.objects.count()
        finish_ingredients = Ingredient.objects.count()

        self.assertEquals(finish_recipe, initial_recipe - 1)
        self.assertEquals(finish_ingredients, initial_ingredients - 1)

    # TODO post?
    # endregion
