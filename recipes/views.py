import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import CreateNewRecipe, IngredientsForm, RecipeIngredientsForm
from .models import Ingredient, Recipe, RecipeIngredient


def recipes_home_page(request):
    user_recipes = Recipe.objects.all().filter(user=request.user.pk)
    context = {"title": "Recipes", "recipes": user_recipes}

    return render(request, "recipes/home.html", context)


class RecipesHomePageView(View):
    template_name = "recipes/home.html"

    def get(self, request):
        user_recipes = Recipe.objects.all().filter(user=request.user.pk).order_by("id")
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
        ingredients = recipe.ingredients.all()
        context = {"form": recipe, "ingredient_form": ingredients}

        return render(request, self.template_name, context)

    def post(self, request, recipe_id):
        form = RecipeIngredientsForm(request.POST)
        if form.is_valid():
            recipe = Recipe.objects.get(id=recipe_id)
            self.ingredients_change(recipe, form)
            changes = self.find_changes(recipe, form)
            if changes is not None:
                for field, (old_value, new_value) in changes.items():
                    setattr(recipe, field, new_value)
            recipe.save()
            messages.success(request, "Przepis został zaktualizowany")
            return redirect("recipes_home_page")

    def ingredients_change(self, recipe, form):
        ingredients_list = list(
            filter(lambda key: key.startswith("quantity-"), form.data)
        )

        old_ingredients = recipe.ingredients.all()
        if len(old_ingredients) == len(ingredients_list):
            for counter, prefix in enumerate(ingredients_list):
                quantity = form.data.get(prefix)
                name = form.data.get(f"{prefix.replace('quantity', 'name')}")
                quantity_type = form.data.get(
                    f"{prefix.replace('quantity', 'quantity_type')}"
                )
                try:
                    ingredient = get_object_or_404(
                        Ingredient,
                        name=name,
                        quantity=quantity,
                        quantity_type=quantity_type,
                    )
                except Http404:
                    ingredient = Ingredient.objects.create(
                        name=name, quantity=quantity, quantity_type=quantity_type
                    )

                if ingredient != old_ingredients[counter]:
                    recipe_ingredient = RecipeIngredient.objects.filter(
                        recipe=recipe, ingredient=old_ingredients[counter]
                    ).first()
                    recipe_ingredient.ingredient = ingredient
                    recipe_ingredient.save()
        elif len(old_ingredients) < len(ingredients_list):
            for prefix in ingredients_list:
                quantity = form.data.get(prefix)
                name = form.data.get(f"{prefix.replace('quantity', 'name')}")
                quantity_type = form.data.get(
                    f"{prefix.replace('quantity', 'quantity_type')}"
                )
                try:
                    ingredient, created = Ingredient.objects.get_or_create(
                        name=name, quantity=quantity, quantity_type=quantity_type
                    )
                    if not recipe.ingredients.filter(id=ingredient.id).exists():
                        RecipeIngredient.objects.create(
                            recipe=recipe, ingredient=ingredient
                        )
                except Exception as e:
                    print(e)
        else:
            recipe_ingredient = RecipeIngredient.objects.filter(recipe=recipe)
            actual_ingredients = []
            for prefix in ingredients_list:
                quantity = form.data.get(prefix)
                name = form.data.get(f"{prefix.replace('quantity', 'name')}")
                quantity_type = form.data.get(
                    f"{prefix.replace('quantity', 'quantity_type')}"
                )
                try:
                    ingredient, created = Ingredient.objects.get_or_create(
                        name=name, quantity=quantity, quantity_type=quantity_type
                    )
                    actual_ingredients.append(ingredient.id)
                    if not recipe.ingredients.filter(id=ingredient.id).exists():
                        RecipeIngredient.objects.create(
                            recipe=recipe, ingredient=ingredient
                        )
                except Exception as e:
                    print(e)

            delete_ingredients = recipe_ingredient.exclude(
                ingredient_id__in=actual_ingredients
            )
            delete_ingredients.delete()

    def find_changes(self, recipe, form):
        changes = {}
        recipe_name_from_recipe = recipe.recipe_name
        recipe_name_from_form = form.data.get("recipe_name")
        preparation_from_recipe = recipe.preparation
        preparation_from_form = form.data.get("preparation")
        tags_from_recipe = recipe.tags
        tags_from_form = [form.data.get("tags")]

        if recipe_name_from_recipe != recipe_name_from_form:
            changes["recipe_name"] = (recipe_name_from_recipe, recipe_name_from_form)
        if preparation_from_recipe != preparation_from_form:
            changes["preparation"] = (preparation_from_recipe, preparation_from_form)
        if tags_from_recipe != tags_from_form:
            changes["tags"] = (tags_from_recipe, tags_from_form)
        return changes


class RecipeDeletePageView(View):
    def get(self, request, recipe_id):
        self.post(request, recipe_id)
        messages.success(request, "Pomyślnie usunięto przepis")
        return redirect("recipes_home_page")

    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.delete()
