from rest_framework import serializers

from ..models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = ["id", "recipe_name", "preparation", "user"]


class RecipeEditSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = ["recipe_name", "recipe_ingredient", "preparation", "user"]
