from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from ingredients.models import Ingredient
from products.factorires import ProductFactory
from products.models import Product
from recipe_ingredients.factories import RecipeIngredientFactory
from recipe_ingredients.models import RecipeIngredient
from recipes.factories import RecipeFactory
from recipes.models import Recipe
from user_ingredients.models import UserIngredient

from ..factories import UserFactory
from ..models import Profile

HOME_PAGE = "home-page"


class TestViews(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.home_page = reverse("home-page")
        self.login_page = reverse("login-page")
        self.register_page = reverse("register-page")
        self.reset_password_page = reverse("reset-password-page")
        self.profile_page = reverse("profile-page")
        self.product_factory = ProductFactory.create()
        self.recipe_ingredient_factory = RecipeIngredientFactory.create()
        self.recipe_factory = RecipeFactory.create(user=self.profile)
        Recipe.objects.get(id=self.recipe_factory.id).recipe_ingredient.add(
            self.recipe_ingredient_factory
        )

    # region tests for home view
    def test_home_page_view_user_not_logged_GET(self):
        response = self.client.get(self.home_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/home.html")
        self.assertContains(response, "Login")
        self.assertContains(response, "Register")

    def test_home_page_view_user_logged_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.home_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/dashboard.html")
        self.assertContains(response, "Dashboard")
        self.assertContains(response, "Recipes")
        self.assertContains(response, "Products")
        self.assertContains(response, "My Ingredients")
        self.assertContains(response, "Home Page")
        self.assertContains(response, self.user.username)
        self.assertContains(response, "Recipe Name")
        self.assertContains(response, self.recipe_factory.recipe_name)
        self.assertContains(response, "Ingredients")
        self.assertContains(response, self.recipe_ingredient_factory.amount)
        self.assertContains(
            response, self.recipe_ingredient_factory.ingredient.quantity_type
        )
        self.assertContains(
            response, self.recipe_ingredient_factory.ingredient.product.name
        )
        self.assertContains(response, "Preparation")
        self.assertContains(response, self.recipe_factory.preparation)
        self.assertContains(response, "Tags")
        self.assertContains(response, self.recipe_factory.tags[0])

    def test_home_page_view_user_logged_with_recipe_without_ingredient_GET(self):
        Product.objects.all().delete()
        Ingredient.objects.all().delete()
        RecipeIngredient.objects.all().delete()
        self.client.force_login(self.user)
        response = self.client.get(self.home_page)
        self.assertNotContains(response, "Recipes, which can be done")
        self.assertNotContains(response, "Missing ingredients in recipes: ")

    def test_home_page_view_user_logged_with_recipe_with_ingredient_GET(self):
        UserIngredient.objects.create(
            user=self.profile,
            ingredient=self.recipe_ingredient_factory.ingredient,
            amount=self.recipe_ingredient_factory.amount,
        )
        self.client.force_login(self.user)
        response = self.client.get(self.home_page)
        self.assertContains(response, "Recipes, which can be done")
        self.assertNotContains(response, "Missing ingredients in recipes: ")

    def test_home_page_view_user_logged_with_recipe_with_not_enough_ingredient_GET(
        self,
    ):
        UserIngredient.objects.create(
            user=self.profile,
            ingredient=self.recipe_ingredient_factory.ingredient,
            amount=self.recipe_ingredient_factory.amount - 1,
        )
        self.client.force_login(self.user)
        response = self.client.get(self.home_page)
        self.assertContains(response, "Missing ingredients in recipes: ")
        self.assertNotContains(response, "Recipes, which can be done")

    def test_home_page_view_user_logged_with_two_recipes_with_not_enough_ingredient_GET(
        self,
    ):
        UserIngredient.objects.create(
            user=self.profile,
            ingredient=self.recipe_ingredient_factory.ingredient,
            amount=self.recipe_ingredient_factory.amount - 1,
        )
        new_recipe_ingredient = RecipeIngredientFactory.create()
        UserIngredient.objects.create(
            user=self.profile,
            ingredient=new_recipe_ingredient.ingredient,
            amount=new_recipe_ingredient.amount - 1,
        )
        new_recipe = Recipe.objects.create(user=self.profile, recipe_name="qwe")
        Recipe.objects.get(id=new_recipe.id).recipe_ingredient.add(
            new_recipe_ingredient
        )

        self.client.force_login(self.user)
        response = self.client.get(self.home_page)
        self.assertContains(response, "Missing ingredients in recipes: ")
        self.assertNotContains(response, "Recipes, which can be done")

    # endregion
    # region tests for login view
    def test_login_page_view_GET(self):
        response = self.client.get(self.login_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login.html")
        self.assertContains(response, "Log In!")
        self.assertContains(response, "Register")
        self.assertContains(response, "Username")
        self.assertContains(response, '<input type="text" name="username"')
        self.assertContains(response, "Password")
        self.assertContains(response, '<input type="password" name="password"')
        self.assertContains(response, "Login")
        self.assertContains(response, "Forget password?")
        self.assertContains(response, "Reset password")
        self.assertContains(response, "/reset_password/")
        self.assertContains(response, "Does not have an account?")
        self.assertContains(response, "/register")

    def test_login_page_view_POST(self):
        login_data = {
            "username": self.user.username,
            "password": "Test1!",
        }
        response = self.client.post(self.login_page, login_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.home_page)
        self.assertContains(response, "Dashboard")
        self.assertContains(response, "Recipes")
        self.assertContains(response, "Products")
        self.assertContains(response, "My Ingredients")
        self.assertContains(response, "Home Page")
        self.assertContains(response, self.user.username)
        self.assertContains(response, "Recipe Name")
        self.assertContains(response, self.recipe_factory.recipe_name)
        self.assertContains(response, "Ingredients")
        self.assertContains(response, self.recipe_ingredient_factory.amount)
        self.assertContains(
            response, self.recipe_ingredient_factory.ingredient.quantity_type
        )
        self.assertContains(
            response, self.recipe_ingredient_factory.ingredient.product.name
        )
        self.assertContains(response, "Preparation")
        self.assertContains(response, self.recipe_factory.preparation)
        self.assertContains(response, "Tags")
        self.assertContains(response, self.recipe_factory.tags[0])

    def test_login_page_view_wrong_username_POST(self):
        login_data = {
            "username": "qwe",
            "password": "Test11!!",
        }
        response = self.client.post(self.login_page, login_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login.html")
        self.assertContains(response, "Log In!")
        self.assertContains(response, "Wrong username or password")
        self.assertContains(response, "Username")
        self.assertContains(response, '<input type="text" name="username" value="qwe"')
        self.assertContains(response, "Password")
        self.assertContains(response, '<input type="password" name="password"')
        self.assertContains(response, "Login")
        self.assertContains(response, "Forget password?")
        self.assertContains(response, "Reset password")
        self.assertContains(response, "/reset_password/")
        self.assertContains(response, "Does not have an account?")
        self.assertContains(response, "/register")

    def test_login_page_view_wrong_password_POST(self):
        login_data = {
            "username": self.user.username,
            "password": "qwerty",
        }
        response = self.client.post(self.login_page, login_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login.html")
        self.assertContains(response, "Log In!")
        self.assertContains(response, "Wrong username or password")
        self.assertContains(response, "Username")
        self.assertContains(
            response, f'<input type="text" name="username" value="{self.user.username}"'
        )
        self.assertContains(response, "Password")
        self.assertContains(response, '<input type="password" name="password"')
        self.assertContains(response, "Login")
        self.assertContains(response, "Forget password?")
        self.assertContains(response, "Reset password")
        self.assertContains(response, "/reset_password/")
        self.assertContains(response, "Does not have an account?")
        self.assertContains(response, "/register")

    def test_login_page_view_both_wrong_credentials_POST(self):
        login_data = {
            "username": "abc",
            "password": "1",
        }
        response = self.client.post(self.login_page, login_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login.html")
        self.assertContains(response, "Log In!")
        self.assertContains(response, "Wrong username or password")
        self.assertContains(response, "Username")
        self.assertContains(response, '<input type="text" name="username" value="abc"')
        self.assertContains(response, "Password")
        self.assertContains(response, '<input type="password" name="password"')
        self.assertContains(response, "Login")
        self.assertContains(response, "Forget password?")
        self.assertContains(response, "Reset password")
        self.assertContains(response, "/reset_password/")
        self.assertContains(response, "Does not have an account?")
        self.assertContains(response, "/register")

    # endregion
    # region tests for register view
    def test_register_page_view_GET(self):
        response = self.client.get(self.register_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register.html")
        self.assertContains(response, "Register form")
        self.assertContains(response, "Username")
        self.assertContains(response, '<input type="text" name="username"')
        self.assertContains(response, "Email")
        self.assertContains(response, '<input type="email" name="email"')
        self.assertContains(response, "Password")
        self.assertContains(response, '<input type="password" name="password1"')
        self.assertContains(response, "Password confirmation")
        self.assertContains(response, '<input type="password" name="password2"')
        self.assertContains(response, "Sign Up")
        self.assertContains(response, "Have an account?")
        self.assertContains(response, self.login_page)

    def test_register_page_view_POST(self):
        register_data = {
            "username": "Test1",
            "email": "test@tt.tt",
            "password1": "Asd123!!",
            "password2": "Asd123!!",
        }
        response = self.client.post(self.register_page, register_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.login_page)
        self.assertContains(response, "User created correctly")

    def test_register_page_view_the_same_user_in_db(self):
        register_data = {
            "username": self.user.username,
            "email": "zxc@zxc.zxc",
            "password1": "Asd123!@#",
            "password2": "Asd123!@#",
        }
        response = self.client.post(self.register_page, register_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.register_page)
        self.assertContains(response, "Form have invalid data")

    def test_register_page_view_the_same_email_in_db_POST(self):
        register_data = {
            "username": "hjk1",
            "email": self.user.email,
            "password1": "Vbg123!",
            "password2": "Vbg123!",
        }
        response = self.client.post(self.register_page, register_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.register_page)
        self.assertContains(response, "Form have invalid data")

    def test_register_page_view_different_passwords_POST(self):
        register_data = {
            "username": "rrr1",
            "email": "rrr@rr.rr",
            "password1": "rrr123!",
            "password2": "rrr123!!",
        }
        response = self.client.post(self.register_page, register_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.register_page)
        self.assertContains(response, "Form have invalid data")

    # endregion
    # region tests for reset_password view
    def test_reset_password_page_view_GET(self):
        response = self.client.get(self.reset_password_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/reset_password.html")
        self.assertContains(response, "Reset password!")
        self.assertContains(response, "Email")
        self.assertContains(response, '<input type="email" name="email"')
        self.assertContains(response, "New password")
        self.assertContains(response, '<input type="password" name="new_password' "")
        self.assertContains(response, "Confirm new password")
        self.assertContains(
            response, '<input type="password" name="confirm_new_password"'
        )
        self.assertContains(response, "Reset")
        self.assertContains(response, "Have an account?")
        self.assertContains(response, self.login_page)
        self.assertContains(response, "Does not have an account?")
        self.assertContains(response, self.register_page)

    def test_reset_password_page_view_POST(self):
        reset_password_form = {
            "email": self.user.email,
            "new_password": "New_P@ss_123",
            "confirm_new_password": "New_P@ss_123",
        }
        response = self.client.post(
            self.reset_password_page, reset_password_form, follow=True
        )
        self.user.refresh_from_db()
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.login_page)
        self.assertContains(response, "Password successfully reset")

    def test_reset_password_page_view_email_not_exist_POST(self):
        reset_password_form = {
            "email": "ee@ee.ee",
            "new_password": "Test1!qqq",
            "confirm_new_password": "Test1!qqq",
        }
        response = self.client.post(
            self.reset_password_page, reset_password_form, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.reset_password_page)
        self.assertContains(response, "Email does not exist")
        self.assertContains(response, "Reset password!")
        self.assertContains(response, "Email")
        self.assertContains(response, '<input type="email" name="email"')
        self.assertContains(response, "New password")
        self.assertContains(response, '<input type="password" name="new_password' "")
        self.assertContains(response, "Confirm new password")
        self.assertContains(
            response, '<input type="password" name="confirm_new_password"'
        )
        self.assertContains(response, "Reset")
        self.assertContains(response, "Have an account?")
        self.assertContains(response, self.login_page)
        self.assertContains(response, "Does not have an account?")
        self.assertContains(response, self.register_page)

    def test_reset_password_page_view_different_passwords_POST(self):
        reset_password_data = {
            "email": self.user.email,
            "new_password": "Qwedsa123!@",
            "confirm_new_password": "Qweasd123!@",
        }
        response = self.client.post(
            self.reset_password_page, reset_password_data, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.reset_password_page)
        self.assertContains(response, "Passwords are not the same")
        self.assertContains(response, "Reset password!")
        self.assertContains(response, "Email")
        self.assertContains(response, '<input type="email" name="email"')
        self.assertContains(response, "New password")
        self.assertContains(response, '<input type="password" name="new_password' "")
        self.assertContains(response, "Confirm new password")
        self.assertContains(
            response, '<input type="password" name="confirm_new_password"'
        )
        self.assertContains(response, "Reset")
        self.assertContains(response, "Have an account?")
        self.assertContains(response, self.login_page)
        self.assertContains(response, "Does not have an account?")
        self.assertContains(response, self.register_page)

    def test_reset_password_page_view_incomplete_form_POST(self):
        reset_password_data = {
            "email": "email@email.pl",
        }
        response = self.client.post(
            self.reset_password_page, reset_password_data, follow=True
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/reset_password.html")
        self.assertContains(response, "Invalid data in reset password form")
        self.assertContains(response, "Reset password!")
        self.assertContains(response, "Email")
        self.assertContains(response, '<input type="email" name="email"')
        self.assertContains(response, "New password")
        self.assertContains(response, '<input type="password" name="new_password' "")
        self.assertContains(response, "Confirm new password")
        self.assertContains(
            response, '<input type="password" name="confirm_new_password"'
        )
        self.assertContains(response, "Reset")
        self.assertContains(response, "Have an account?")
        self.assertContains(response, self.login_page)
        self.assertContains(response, "Does not have an account?")
        self.assertContains(response, self.register_page)

    # endregion
