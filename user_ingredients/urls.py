from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .api.views import UserIngredientViewSet
from .views import (
    UserIngredientsAddPageView,
    UserIngredientsDeletePageView,
    UserIngredientsEditPageView,
    UserIngredientsHomePageView,
)

app_name = "my_ingredients"

router = SimpleRouter()
router.register("user-ingredients", UserIngredientViewSet)

urlpatterns = [
    path(
        "my-ingredients/",
        UserIngredientsHomePageView.as_view(),
        name="useringredients-home-page",
    ),
    path(
        "my-ingredients/add/",
        UserIngredientsAddPageView.as_view(),
        name="useringredient-add",
    ),
    path(
        "my-ingredients/add/<int:product_id>",
        UserIngredientsAddPageView.as_view(),
        name="useringredient-add",
    ),
    path(
        "my-ingredients/<int:my_ingredient_id>/edit/",
        UserIngredientsEditPageView.as_view(),
        name="useringredient-edit",
    ),
    path(
        "my-ingredients/<int:my_ingredient_id>/edit/<int:product_id>",
        UserIngredientsEditPageView.as_view(),
        name="useringredient-edit",
    ),
    path(
        "my-ingredients/<int:pk>/delete/",
        UserIngredientsDeletePageView.as_view(),
        name="useringredient-delete",
    ),
    path("api/", include(router.urls)),
]
