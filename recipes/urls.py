from django.urls import include, path

from . import views
from .views import RecipeAddPageView, RecipesHomePageView

urlpatterns = [
    path("", RecipesHomePageView.as_view(), name="recipes_home_page"),
    path("add/", RecipeAddPageView.as_view(), name="recipes_add"),
]
