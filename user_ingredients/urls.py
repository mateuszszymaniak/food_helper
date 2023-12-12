from django.urls import path

from .views import (
    UserIngredientsAddPageView,
    UserIngredientsDeletePageView,
    UserIngredientsEditPageView,
    UserIngredientsHomePageView,
)

app_name = "my_ingredients"

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
        "my-ingredients/<int:my_ingredient_id>/edit/",
        UserIngredientsEditPageView.as_view(),
        name="useringredient-edit",
    ),
    path(
        "my-ingredients/<int:pk>/delete/",
        UserIngredientsDeletePageView.as_view(),
        name="useringredient-delete",
    ),
]
