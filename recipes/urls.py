from django.urls import include, path

from . import views
from .views import RecipeAddPageView, RecipeEditPageView, RecipesHomePageView

urlpatterns = [
    path("", RecipesHomePageView.as_view(), name="recipes_home_page"),
    path("add/", RecipeAddPageView.as_view(), name="recipes_add"),
    path("edit/<int:recipe_id>/", RecipeEditPageView.as_view(), name="recipe_edit"),
]
