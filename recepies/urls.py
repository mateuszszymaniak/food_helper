from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.recepies_home_page, name="recepies_home_page"),
    path("add/", views.recepies_add, name="recepies_add"),
]
