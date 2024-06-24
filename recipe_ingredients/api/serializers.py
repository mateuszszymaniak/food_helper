from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import RecipeIngredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=RecipeIngredient.objects.all(),
                fields=("amount", "ingredient"),
                message="Recipe ingredient has been inserted earlier",
            )
        ]

    # def validate(self, attrs):
    #     if self.instance:
    #         self.instance.amount = attrs['amount']
    #         self.instance.ingredient = attrs['ingredient']
    #         attrs['msg'] = "Recipe ingredient has been updated"
    #     else:
    #         recipe_ingredient, create = RecipeIngredient.objects.get_or_create(ingredient=attrs['ingredient'], amount=attrs['amount'])
    #         if create:
    #             attrs['id'] = recipe_ingredient.id
    #         attrs['msg'] = "Recipe ingredient has been added"
    #     return attrs
