from rest_framework import serializers

from ..models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    # def validate(self, attrs):
    #     product, create = Product.objects.get_or_create(name=attrs['name'])
    #     if not create:
    #         attrs['msg'] = "Product exist"
    #     else:
    #         attrs['msg'] = "Product has been added"
    #     return attrs
