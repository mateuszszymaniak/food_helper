from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from .forms import CreateNewRecipe
from .models import Recipe


class RecipesHomePageView(LoginRequiredMixin, View):
    template_name = "recipes/home.html"

    def get(self, request):
        user_recipes = Recipe.objects.filter(user=request.user.pk).order_by("id")
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
        context = {
            "title": "Recipes",
            "recipes": recipes_with_ingredients,
        }
        return render(request, self.template_name, context)


class RecipeAddPageView(LoginRequiredMixin, View):
    template_name = "recipes/recipe_form.html"

    def get(self, request):
        form = CreateNewRecipe()
        context = {"title": "Add Recipe", "form": form}

        return render(request, self.template_name, context)

    def post(self, request):
        form = CreateNewRecipe(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user.profile
            recipe.save()
            if "add_ingredient" in request.POST:
                return redirect("ingredient-add", recipe.id)
            else:
                messages.success(request, "Przepis został dodany")
                return redirect("recipes-home-page")
        else:
            messages.warning(request, "Invalid data in recipe")
            return redirect("recipe-add")


class RecipeEditPageView(LoginRequiredMixin, View):
    template_name = "recipes/recipe_form.html"

    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        ingredients = recipe.ingredients.all()
        context = {
            "title": "Edit Recipe",
            "form": recipe,
            "ingredient_form": ingredients,
        }

        return render(request, self.template_name, context)

    def post(self, request, recipe_id):
        form = CreateNewRecipe(request.POST)
        if form.is_valid():
            Recipe.objects.filter(id=recipe_id).update(
                recipe_name=request.POST.get("recipe_name"),
                preparation=request.POST.get("preparation"),
                tags=[request.POST.get("tags")],
            )
            if "add_ingredient" in request.POST:
                return redirect("ingredients:ingredient-add", recipe_id)
            else:
                messages.success(request, "Przepis został zaktualizowany")
                return redirect("recipes-home-page")
        else:
            messages.warning(request, "Invalid data in recipe")
            return redirect("recipe-edit")


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy("recipes-home-page")

    def form_valid(self, form):
        messages.success(self.request, "Pomyślnie usunięto przepis")
        return super().form_valid(form)
