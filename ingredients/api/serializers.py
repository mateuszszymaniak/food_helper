from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=Ingredient.objects.all(),
                fields=("product", "quantity_type"),
                message="Ingredient exists - use get method with parameters",
            )
        ]
