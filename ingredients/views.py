from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from recipes.models import Recipe

from .forms import IngredientsForm
from .models import Ingredient


class IngredientAddView(LoginRequiredMixin, View):
    template_name = "ingredients/ingredient_form.html"

    def get(self, request, recipe_id):
        form = IngredientsForm()
        context = {"title": "Add Ingredient", "form": form}

        return render(request, self.template_name, context)

    def post(self, request, recipe_id):
        form = IngredientsForm(request.POST)
        if form.is_valid():
            recipe = Recipe.objects.get(id=recipe_id)
            ingredient = form.save()
            recipe.ingredients.add(ingredient.id)
            return redirect("recipe-edit", recipe_id)


class IngredientEditView(LoginRequiredMixin, View):
    template_name = "ingredients/ingredient_form.html"

    def get(self, request, recipe_id, ingredient_id):
        ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
        context = {"form": ingredient}

        return render(request, self.template_name, context)

    def post(self, request, recipe_id, ingredient_id):
        form = IngredientsForm(request.POST)
        if form.is_valid():
            Ingredient.objects.filter(id=ingredient_id).update(
                name=request.POST.get("name"),
                quantity=request.POST.get("quantity"),
                quantity_type=request.POST.get("quantity_type"),
            )
            return redirect("recipe-edit", recipe_id)
