from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import UserIngredient
from .serializers import UserIngredientSerializer


class UserIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = UserIngredientSerializer
    queryset = UserIngredient.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
