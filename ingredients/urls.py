from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .api.views import IngredientViewSet

router = SimpleRouter()
router.register("ingredients", IngredientViewSet)

urlpatterns = [path("api/", include(router.urls))]
