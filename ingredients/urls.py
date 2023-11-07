from django.urls import path

from .views import IngredientAddView, IngredientEditView

urlpatterns = [
    path(
        "recipe/<int:recipe_id>/add_ingredient",
        IngredientAddView.as_view(),
        name="ingredient-add",
    ),
    path(
        "recipe/<int:recipe_id>/edit_ingredient/<int:ingredient_id>",
        IngredientEditView.as_view(),
        name="ingredient-edit",
    ),
]
