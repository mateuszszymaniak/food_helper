from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CreateNewRecipe
from .models import Recipe


class RecipesHomePageView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/home.html"
    extra_context = {"title": "Recipes"}

    def get(self, request, *args, **kwargs):
        user_recipes = self.model.objects.filter(user=request.user.pk).order_by("id")
        recipes_with_ingredients = []
        for recipe in user_recipes:
            recipe_data = {
                "id": recipe.id,
                "recipe_name": recipe.recipe_name,
                "preparation": recipe.preparation,
                "tags": recipe.tags,
                "ingredients": [],
            }

            ingredients = recipe.recipe_ingredient.all()

            for ingredient in ingredients:
                ingredient_data = {
                    "name": ingredient.ingredient.product.name,
                    "quantity": ingredient.amount,
                    "quantity_type": ingredient.ingredient.quantity_type,
                }
                recipe_data["ingredients"].append(ingredient_data)
            recipes_with_ingredients.append(recipe_data)
        context = self.extra_context
        context["recipes"] = recipes_with_ingredients
        return render(request, self.template_name, context)


class RecipeAddPageView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = CreateNewRecipe
    template_name = "recipes/recipe_form.html"
    extra_context = {"title": "Add Recipe"}

    def get(self, request, *args, **kwargs):
        context = self.extra_context
        context["form"] = self.form_class
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.user = request.user.profile
            recipe = form.save()
            if "add_ingredient" in request.POST:
                return redirect("recipe_ingredients:ingredient-add", recipe.id)
            else:
                messages.success(request, "Recipe has been added")
                return redirect("recipes-home-page")
        else:
            messages.warning(request, "Invalid data in recipe")
            return redirect("recipe-add")


class RecipeEditPageView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = CreateNewRecipe
    template_name = "recipes/recipe_form.html"
    extra_context = {"title": "Edit Recipe"}

    def get(self, request, *args, **kwargs):
        recipe_id = kwargs.get("recipe_id")
        recipe = get_object_or_404(self.model, pk=recipe_id)
        context = self.extra_context
        context["form"] = self.form_class(
            initial={
                "recipe_name": recipe.recipe_name,
                "preparation": recipe.preparation,
                "tags": recipe.tags,
                "recipe_id": recipe_id,
            }
        )
        context["ingredients"] = recipe.recipe_ingredient.all().order_by("id")
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        recipe_id = kwargs.get("recipe_id")
        form = self.form_class(request.POST)
        if form.is_valid():
            self.model.objects.filter(id=recipe_id).update(
                recipe_name=form.cleaned_data.get("recipe_name"),
                preparation=form.cleaned_data.get("preparation"),
                tags=form.cleaned_data.get("tags"),
            )
            if "add_ingredient" in request.POST:
                return redirect("recipe_ingredients:ingredient-add", recipe_id)
            messages.success(request, "Recipe has been updated")
            return redirect("recipes-home-page")
        else:
            messages.warning(request, "Invalid data in recipe")
            return redirect("recipe-edit", recipe_id)


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy("recipes-home-page")

    def form_valid(self, form):
        messages.success(self.request, "Successfully remove recipe")
        return super().form_valid(form)
