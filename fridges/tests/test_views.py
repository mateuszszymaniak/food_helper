from http import HTTPStatus

from django.test import TestCase, tag
from django.urls import reverse

from ingredients.factories import IngredientFactory
from users.factories import UserFactory
from users.models import Profile

from ..models import Fridge


class FridgeViews(TestCase):
    def setUp(self):
        self.fridge_home_page = reverse("fridges-home-page")
        self.fridge_add_page = reverse("fridge-add")
        self.user1 = UserFactory.create()
        self.profile1, _ = Profile.objects.get_or_create(user=self.user1)
        self.client.force_login(self.user1)
        self.ingredient_factory = IngredientFactory.create()
        self.ingredient = Fridge.objects.create(
            name=self.ingredient_factory.name,
            quantity=self.ingredient_factory.quantity,
            quantity_type=self.ingredient_factory.quantity_type,
            user=self.profile1,
        )
        self.fridge_edit = reverse("fridge-edit", args=[self.ingredient.id])
        self.fridge_delete = reverse("fridge-delete", args=[self.ingredient.id])

    # region tests for home view
    def test_fridge_home_page_view_GET_with_empty_fridge(self):
        Fridge.objects.all().delete()

        response = self.client.get(self.fridge_home_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "fridges/home.html")
        self.assertContains(response, "Add items from fridge")

    def test_fridge_home_page_view_GET_with_fridge(self):
        response = self.client.get(self.fridge_home_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "fridges/home.html")
        self.assertContains(response, "Quantity")

    # endregion
    # region tests for add view
    def test_fridge_add_page_view_GET(self):
        response = self.client.get(self.fridge_add_page)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "fridges/fridge_form.html")

    def test_fridge_add_page_view_POST_correct_data(self):
        Fridge.objects.all().delete()

        ingredient = IngredientFactory.create()
        ingredient_data = {
            "name": ingredient.name,
            "quantity": ingredient.quantity,
            "quantity_type": ingredient.quantity_type,
        }
        response = self.client.post(self.fridge_add_page, ingredient_data, follow=True)
        self.assertEquals(Fridge.objects.count(), 1)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Ingredient has been added to fridge")
        self.assertRedirects(response, expected_url=self.fridge_home_page)

    def test_fridge_add_page_view_POST_add_amount_to_existing_ingredient(self):
        ingredient_data = {
            "name": self.ingredient.name,
            "quantity": "1",
            "quantity_type": self.ingredient.quantity_type,
        }

        response = self.client.post(self.fridge_add_page, ingredient_data, follow=True)
        self.assertEquals(
            Fridge.objects.get(name=self.ingredient.name).quantity,
            str(int(self.ingredient.quantity) + int(ingredient_data.get("quantity"))),
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Ingredient has been added to fridge")
        self.assertRedirects(response, expected_url=self.fridge_home_page)

    def test_fridge_add_page_view_POST_missing_name_in_form(self):
        ingredient_data = {
            "quantity": self.ingredient.quantity,
            "quantity_type": self.ingredient.quantity_type,
        }
        response = self.client.post(self.fridge_add_page, ingredient_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Invalid data in ingredient")
        self.assertRedirects(response, expected_url=self.fridge_add_page)

    def test_fridge_add_page_view_POST_missing_quantity_in_form(self):
        ingredient_data = {
            "name": self.ingredient.name,
            "quantity_type": self.ingredient.quantity_type,
        }
        response = self.client.post(self.fridge_add_page, ingredient_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Invalid data in ingredient")
        self.assertRedirects(response, expected_url=self.fridge_add_page)

    def test_fridge_add_page_view_POST_missing_quantity_type_in_form(self):
        ingredient_data = {
            "name": self.ingredient.name,
            "quantity": self.ingredient.quantity,
        }
        response = self.client.post(self.fridge_add_page, ingredient_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Invalid data in ingredient")
        self.assertRedirects(response, expected_url=self.fridge_add_page)

    # endregion
    # region tests for edit view
    def test_fridge_edit_page_view_GET(self):
        response = self.client.get(self.fridge_edit)
        self.assertContains(response, self.ingredient.name)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "fridges/fridge_form.html")

    def test_fridge_edit_page_view_POST_correct_data(self):
        ingredient_data = {
            "name": "ing1_edit",
            "quantity": self.ingredient.quantity,
            "quantity_type": self.ingredient.quantity_type,
        }
        response = self.client.post(self.fridge_edit, ingredient_data, follow=True)
        self.assertEquals(Fridge.objects.get(id=self.ingredient.id).name, "ing1_edit")
        self.assertEquals(
            Fridge.objects.get(id=self.ingredient.id).quantity,
            str(self.ingredient.quantity),
        )
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Ingredient has been updated")
        self.assertRedirects(response, expected_url=self.fridge_home_page)

    # endregion
    # region tests for delete view
    def test_delete_fridge(self):
        response = self.client.post(self.fridge_delete, follow=True)
        self.assertEquals(Fridge.objects.count(), 0)
        self.assertContains(response, "Successfully removed ingredient")
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.fridge_home_page)

    # endregion
