from http import HTTPStatus

from django.test import TestCase, tag
from django.urls import reverse

from recipes.factories import IngredientFactory
from users.models import Profile, User

from ..models import Fridge


class FridgeViews(TestCase):
    def setUp(self):
        self.fridge_home_page = reverse("fridges-home-page")
        self.fridge_add_page = reverse("fridge-add")
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
        self.ingredient1_name = "ing1"
        self.ingredient1_quantity = "2"
        self.ingredient1_quantity_type = "kg"
        self.ingredient1 = Fridge.objects.create(
            name=self.ingredient1_name,
            quantity=self.ingredient1_quantity,
            quantity_type=self.ingredient1_quantity_type,
            user=self.profile1,
        )
        self.fridge_edit = reverse("fridge-edit", args=[self.ingredient1.id])
        self.fridge_delete = reverse("fridge-delete", args=[self.ingredient1.id])

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
            "name-0": ingredient.name,
            "quantity-0": ingredient.quantity,
            "quantity_type-0": ingredient.quantity_type,
        }
        response = self.client.post(self.fridge_add_page, ingredient_data, follow=True)
        self.assertEquals(Fridge.objects.count(), 1)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Zawartość lodówki została dodana")
        self.assertRedirects(response, expected_url=self.fridge_home_page)

    def test_fridge_add_page_view_POST_add_amount_to_existing_ingredient(self):
        ingredient_data = {
            "name-0": self.ingredient1_name,
            "quantity-0": "1",
            "quantity_type-0": self.ingredient1_quantity_type,
        }

        response = self.client.post(self.fridge_add_page, ingredient_data, follow=True)
        self.assertEquals(Fridge.objects.get(name=self.ingredient1_name).quantity, "3")
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Zawartość lodówki została dodana")
        self.assertRedirects(response, expected_url=self.fridge_home_page)

    # endregion
    # region tests for edit view
    def test_fridge_edit_page_view_GET(self):
        response = self.client.get(self.fridge_edit)
        self.assertContains(response, self.ingredient1_name)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "fridges/fridge_form.html")

    def test_fridge_edit_page_view_POST(self):
        ingredient_data = {
            "name-0": "ing1_edit",
            "quantity-0": self.ingredient1_quantity,
            "quantity_type-0": self.ingredient1_quantity_type,
        }
        response = self.client.post(self.fridge_edit, ingredient_data, follow=True)
        self.assertEquals(Fridge.objects.get(id=self.ingredient1.id).name, "ing1_edit")
        self.assertEquals(Fridge.objects.get(id=self.ingredient1.id).quantity, "2")
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Składnik został zaktualizowany")
        self.assertRedirects(response, expected_url=self.fridge_home_page)

    # endregion
    # region tests for delete view
    def test_delete_fridge(self):
        response = self.client.post(self.fridge_delete, follow=True)
        self.assertEquals(Fridge.objects.count(), 0)
        self.assertContains(response, "Pomyślnie usunięto składnik")
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, expected_url=self.fridge_home_page)

    # endregion
