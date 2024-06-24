from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Product
from .serializers import ProductSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
