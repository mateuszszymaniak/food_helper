from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from recipes.models import Recipe

from .forms import IngredientsForm
from .models import Ingredient


class IngredientAddView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientsForm
    template_name = "ingredients/ingredient_form.html"
    extra_context = {"title": "Add Recipe Ingredient"}

    def get(self, request, *args, **kwargs):
        context = self.extra_context
        context["form"] = self.form_class
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        recipe_id = kwargs.get("recipe_id")
        form = self.form_class(request.POST)
        if form.is_valid():
            recipe = Recipe.objects.get(id=recipe_id)
            ingredient = form.save()
            recipe.ingredients.add(ingredient.id)
            messages.success(self.request, "Successfully added ingredient")
            return redirect("recipe-edit", recipe_id)
        else:
            messages.warning(request, "Invalid data in ingredient")
            return redirect("ingredients:ingredient-add", recipe_id)


class IngredientEditView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientsForm
    template_name = "ingredients/ingredient_form.html"
    extra_context = {"title": "Edit Recipe Ingredient"}

    def get(self, request, *args, **kwargs):
        ingredient_id = kwargs.get("ingredient_id")
        ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
        context = self.extra_context
        context["form"] = ingredient
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        ingredient_id = kwargs.get("ingredient_id")
        recipe_id = kwargs.get("recipe_id")
        form = self.form_class(request.POST)
        if form.is_valid():
            self.model.objects.filter(id=ingredient_id).update(
                name=form.cleaned_data.get("name"),
                quantity=form.cleaned_data.get("quantity"),
                quantity_type=form.cleaned_data.get("quantity_type"),
            )
            messages.success(self.request, "Successfully edited ingredient")
            return redirect("recipe-edit", recipe_id)
        else:
            messages.warning(request, "Invalid data in ingredient")
            return redirect("ingredients:ingredient-edit", recipe_id, ingredient_id)


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient

    def get_success_url(self):
        recipe_id = self.kwargs["recipe_id"]
        success_url = reverse("recipe-edit", kwargs={"recipe_id": recipe_id})

        return success_url

    def form_valid(self, form):
        messages.success(self.request, "Successfully removed ingredient")
        return super().form_valid(form)
