from django.urls import path

from .views import (
    RecipeAddPageView,
    RecipeDeleteView,
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
        "recipes/<int:pk>/delete/",
        RecipeDeleteView.as_view(),
        name="recipe-delete",
    ),
]
