from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("", include("recipes.urls")),
    path("", include("products.urls")),
    path("", include("user_ingredients.urls")),
    path("", include("recipe_ingredients.urls")),
    path("", include("ingredients.urls")),
]
