from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DeleteView

from recipes.models import Recipe

from .forms import IngredientsForm
from .models import Ingredient


class IngredientAddView(LoginRequiredMixin, View):
    template_name = "ingredients/ingredient_form.html"

    def get(self, request, recipe_id):
        form = IngredientsForm()
        context = {"title": "Add Recipe Ingredient", "form": form}

        return render(request, self.template_name, context)

    def post(self, request, recipe_id):
        form = IngredientsForm(request.POST)
        if form.is_valid():
            recipe = Recipe.objects.get(id=recipe_id)
            ingredient = form.save()
            recipe.ingredients.add(ingredient.id)
            messages.success(self.request, "Successfully added ingredient")
            return redirect("recipe-edit", recipe_id)
        else:
            messages.warning(request, "Invalid data in ingredient")
            return redirect("ingredients:ingredient-add", recipe_id)


class IngredientEditView(LoginRequiredMixin, View):
    template_name = "ingredients/ingredient_form.html"

    def get(self, request, recipe_id, ingredient_id):
        ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
        context = {"title": "Edit Recipe Ingredient", "form": ingredient}

        return render(request, self.template_name, context)

    def post(self, request, recipe_id, ingredient_id):
        form = IngredientsForm(request.POST)
        if form.is_valid():
            Ingredient.objects.filter(id=ingredient_id).update(
                name=request.POST.get("name"),
                quantity=request.POST.get("quantity"),
                quantity_type=request.POST.get("quantity_type"),
            )
            messages.success(self.request, "Successfully edited ingredient")
            return redirect("recipe-edit", recipe_id)
        else:
            messages.warning(request, "Invalid data in ingredient")
            return redirect("ingredients:ingredient-edit", recipe_id)


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient

    def get_success_url(self):
        recipe_id = self.kwargs["recipe_id"]
        success_url = reverse("recipe-edit", kwargs={"recipe_id": recipe_id})

        return success_url

    def form_valid(self, form):
        messages.success(self.request, "Successfully removed ingredient")
        return super().form_valid(form)
