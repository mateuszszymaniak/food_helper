from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ingredients.api.serializers import IngredientSerializer
from ingredients.models import Ingredient


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticated]
