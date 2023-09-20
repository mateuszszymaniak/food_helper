from django.urls import path

from .views import (
    FridgeAddPageView,
    FridgesHomePageView,
    IngredientDeletePageView,
    IngredientEditPageView,
)

urlpatterns = [
    path("fridges/", FridgesHomePageView.as_view(), name="fridges-home-page"),
    path("fridges/add/", FridgeAddPageView.as_view(), name="fridge-add"),
    path(
        "fridges/<int:ingredient_id>/edit/",
        IngredientEditPageView.as_view(),
        name="fridge-edit",
    ),
    path(
        "fridges/<int:ingredient_id>/delete/",
        IngredientDeletePageView.as_view(),
        name="fridge-delete",
    ),
]
