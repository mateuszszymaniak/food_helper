from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import UserIngredient


class UserIngredientSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserIngredient
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=UserIngredient.objects.all(),
                fields=("user", "ingredient"),
                message="Your ingredient has been inserted earlier",
            )
        ]
