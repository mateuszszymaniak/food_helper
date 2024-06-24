from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .api.views import ProductsViewSet
from .views import (
    ProductAddPageView,
    ProductDeleteView,
    ProductEditPageView,
    ProductHomePageView,
)

app_name = "products"

router = SimpleRouter()
router.register("products", ProductsViewSet)

urlpatterns = [
    path("product/", ProductHomePageView.as_view(), name="products-home-page"),
    path("product/add/", ProductAddPageView.as_view(), name="product-add"),
    path(
        "product/<int:product_id>/edit/",
        ProductEditPageView.as_view(),
        name="product-edit",
    ),
    path(
        "product/<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product-delete",
    ),
    path("api/", include(router.urls)),
]
