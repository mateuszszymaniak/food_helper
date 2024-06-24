from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .api.views import RecipeEditViewSet, RecipeViewSet
from .views import (
    RecipeAddPageView,
    RecipeDeleteView,
    RecipeEditPageView,
    RecipesHomePageView,
)

router = SimpleRouter()
router.register("recipes", RecipeViewSet)

urlpatterns = [
    path("recipes/", RecipesHomePageView.as_view(), name="recipes-home-page"),
    path("recipes/add/", RecipeAddPageView.as_view(), name="recipe-add"),
    path(
        "recipes/<int:pk>/edit/",
        RecipeEditPageView.as_view(),
        name="recipe-edit",
    ),
    path(
        "recipes/<int:pk>/delete/",
        RecipeDeleteView.as_view(),
        name="recipe-delete",
    ),
    path("api/", include(router.urls)),
    path(
        "api/recipes/<int:pk>/edit/",
        RecipeEditViewSet.as_view({"put": "update"}),
        name="recipe-edit",
    ),
]
