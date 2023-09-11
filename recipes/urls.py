from django.urls import path, include
from . import views
from .views import recepie_edit

urlpatterns = [
    path("", views.recipes_home_page, name="recipes_home_page"),
    path("add/", views.recipes_add, name="recipes_add"),
    path("edit/<int:recepie_id>/", views.recepie_edit, name="recepie_edit"),
]
