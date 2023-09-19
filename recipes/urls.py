from django.urls import path

from .views import (
    RecipeAddPageView,
    RecipeDeletePageView,
    RecipeEditPageView,
    RecipesHomePageView,
)

urlpatterns = [
    path("recipes/", RecipesHomePageView.as_view(), name="recipes-home-page"),
    path("recipes/add/", RecipeAddPageView.as_view(), name="recipe-add"),
    path(
        "recipes/<int:recipe_id>/edit/",
        RecipeEditPageView.as_view(),
        name="recipe-edit",
    ),
    path(
        "recipes/<int:recipe_id>/delete/",
        RecipeDeletePageView.as_view(),
        name="recipe-delete",
    ),
]
