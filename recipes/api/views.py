from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Recipe
from .serializers import RecipeEditSerializer, RecipeSerializer


class RecipeViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class RecipeEditViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    serializer_class = RecipeEditSerializer
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]
