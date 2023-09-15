from django.urls import include, path

from . import views
from .views import RecipesHomePageView

urlpatterns = [
    path("", RecipesHomePageView.as_view(), name="recipes_home_page"),
    path("add/", views.recipes_add, name="recipes_add"),
]
