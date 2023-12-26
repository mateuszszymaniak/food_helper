from django.urls import path

from .views import (
    ProductAddPageView,
    ProductDeleteView,
    ProductEditPageView,
    ProductHomePageView,
)

app_name = "products"

urlpatterns = [
    path("product/", ProductHomePageView.as_view(), name="products-home-page"),
    path("product/add/", ProductAddPageView.as_view(), name="product-add"),
    path(
        "product/add/<int:recipe_id>", ProductAddPageView.as_view(), name="product-add"
    ),
    path("product/add/<str:new>", ProductAddPageView.as_view(), name="product-add"),
    path(
        "product/add/<int:my_ingredient_id>",
        ProductAddPageView.as_view(),
        name="product-add",
    ),
    path(
        "product/add/<int:recipe_id>/<int:ingredient_id>",
        ProductAddPageView.as_view(),
        name="product-add",
    ),
    path(
        "product/<int:product_id>/edit/",
        ProductEditPageView.as_view(),
        name="product-edit",
    ),
    path(
        "product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"
    ),
]
