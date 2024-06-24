from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import RecipeIngredient
from .serializers import RecipeIngredientSerializer


class RecipeIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeIngredientSerializer
    queryset = RecipeIngredient.objects.all()
    permission_classes = [IsAuthenticated]
