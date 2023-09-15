import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import CreateNewRecipe, IngredientsForm, RecipeIngredientsForm
from .models import Ingredient, Recipe


def recipes_home_page(request):
    user_recipes = Recipe.objects.all().filter(user=request.user.pk)
    context = {"title": "Recipes", "recipes": user_recipes}

    return render(request, "recipes/home.html", context)


class RecipesHomePageView(View):
    template_name = "recipes/home.html"

    def get(self, request):
        user_recipes = Recipe.objects.all().filter(user=request.user.pk)
        recipes_with_ingredients = []
        for recipe in user_recipes:
            recipe_data = {
                "id": recipe.id,
                "recipe_name": recipe.recipe_name,
                "preparation": recipe.preparation,
                "tags": recipe.tags,
                "ingredients": [],
            }

            ingredients = recipe.ingredients.all()

            for ingredient in ingredients:
                ingredient_data = {
                    "name": ingredient.name,
                    "quantity": ingredient.quantity,
                    "quantity_type": ingredient.quantity_type,
                }
                recipe_data["ingredients"].append(ingredient_data)
            recipes_with_ingredients.append(recipe_data)
        context = {"title": "Recipes", "recipes": recipes_with_ingredients}

        return render(request, self.template_name, context)


class RecipeAddPageView(View):
    template_name = "recipes/recipe_form.html"

    @method_decorator(login_required)
    def get(self, request):
        form = RecipeIngredientsForm()
        context = {"title": "Add Recipe", "form": form}

        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        form = RecipeIngredientsForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user.profile
            recipe.save()
            self.add_ingredients_to_recipe(request.POST, recipe)
            messages.success(request, "Przepis został dodany")
            return redirect("recipes_home_page")

    def add_ingredients_to_recipe(self, request, recipe):
        ingredients_list = list(
            filter(lambda key: key.startswith("quantity-"), request)
        )
        for prefix in ingredients_list:
            quantity = request.get(prefix)
            name = request.get(f"{prefix.replace('quantity', 'name')}")
            quantity_type = request.get(
                f"{prefix.replace('quantity', 'quantity_type')}"
            )

            ingredient = Ingredient.objects.get_or_create(
                name=name, quantity=quantity, quantity_type=quantity_type
            )
            recipe.ingredients.add(ingredient[0].id)


class RecipeEditPageView(View):
    template_name = "recipes/recipe_form.html"

    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        ingredients = json.loads(recipe.ingredients)
        form = CreateNewRecipe(instance=recipe)
        ingredient_form = IngredientsForm(instance=ingredients)
        context = {"form": form, "ingredient_form": ingredient_form}

        return render(request, self.template_name, context)
