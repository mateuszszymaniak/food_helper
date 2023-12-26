from django.urls import path

from .views import (
    RecipeIngredientAddView,
    RecipeIngredientDeleteView,
    RecipeIngredientEditView,
)

app_name = "recipe_ingredients"

urlpatterns = [
    path(
        "recipe-ingredient/<int:recipe_id>/add-ingredient",
        RecipeIngredientAddView.as_view(),
        name="ingredient-add",
    ),
    path(
        "recipe-ingredient/<int:recipe_id>/add-ingredient/<int:product_id>",
        RecipeIngredientAddView.as_view(),
        name="ingredient-add",
    ),
    path(
        "recipe-ingredient/<int:recipe_id>/edit-ingredient/<int:ingredient_id>",
        RecipeIngredientEditView.as_view(),
        name="ingredient-edit",
    ),
    path(
        "recipe-ingredient/<int:recipe_id>/edit-ingredient/<int:ingredient_id>/<int:product_id>",
        RecipeIngredientEditView.as_view(),
        name="ingredient-edit",
    ),
    path(
        "recipe-ingredient/<int:recipe_id>/delete-ingredient/<int:pk>",
        RecipeIngredientDeleteView.as_view(),
        name="ingredient-delete",
    ),
]
