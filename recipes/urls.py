from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.recipes_home_page, name="recipes_home_page"),
    path("add/", views.recipes_add, name="recipes_add"),
]
