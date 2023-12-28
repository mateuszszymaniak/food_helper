from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from ingredients.forms import IngredientsForm
from ingredients.models import Ingredient
from products.models import Product
from recipes.models import Recipe

from .models import RecipeIngredients


class RecipeIngredientAddView(LoginRequiredMixin, CreateView):
    model = RecipeIngredients
    form_class = IngredientsForm
    template_name = "recipe_ingredients/ingredient_form.html"
    extra_context = {"title": "Add Recipe Ingredient"}

    def get(self, request, *args, **kwargs):
        context = self.extra_context
        if kwargs.get("product_id"):
            product_id = kwargs.get("product_id")
            context["form"] = self.form_class(initial={"product_name": product_id})
        else:
            context["form"] = self.form_class
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        recipe_id = kwargs.get("recipe_id")
        form = self.form_class(request.POST)
        if "add_product" in request.POST:
            return redirect("products:product-add", recipe_id)
        if form.is_valid():
            recipe = Recipe.objects.get(id=recipe_id)
            ingredient, created = Ingredient.objects.get_or_create(
                product=form.cleaned_data.get("product_name"),
                quantity_type=form.cleaned_data.get("quantity_type"),
            )
            recipe_ingredient, created = self.model.objects.get_or_create(
                ingredient=ingredient, amount=form.cleaned_data.get("amount")
            )
            recipe.recipe_ingredient.add(recipe_ingredient.id)
            messages.success(request, "Successfully added ingredient")
            return redirect("recipe-edit", recipe_id)
        else:
            messages.warning(request, "Invalid data in ingredient")
            return redirect("recipe_ingredients:ingredient-add", recipe_id)


class RecipeIngredientEditView(LoginRequiredMixin, UpdateView):
    model = RecipeIngredients
    form_class = IngredientsForm
    template_name = "recipe_ingredients/ingredient_form.html"
    extra_context = {"title": "Edit Recipe Ingredient"}

    def get(self, request, *args, **kwargs):
        ingredient_id = kwargs.get("ingredient_id")
        recipe_ingredient = get_object_or_404(self.model, pk=ingredient_id)
        context = self.extra_context
        if kwargs.get("product_id"):
            product_id = kwargs.get("product_id")
            recipe_ingredient.product = Product.objects.get(id=product_id)
        context["form"] = self.form_class(
            initial={
                "product_name": recipe_ingredient.ingredient.product,
                "quantity_type": recipe_ingredient.ingredient.quantity_type,
                "amount": self.model.objects.get(id=ingredient_id).amount,
            }
        )
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        ingredient_id = kwargs.get("ingredient_id")
        recipe_id = kwargs.get("recipe_id")
        form = self.form_class(request.POST)
        if "add_product" in request.POST:
            return redirect("products:product-add", recipe_id, ingredient_id)
        if form.is_valid():
            ingredient, created = Ingredient.objects.get_or_create(
                product=form.cleaned_data.get("product_name"),
                quantity_type=form.cleaned_data.get("quantity_type"),
            )
            self.model.objects.filter(id=ingredient_id).update(
                ingredient=ingredient, amount=form.cleaned_data.get("amount")
            )
            messages.success(request, "Successfully edited ingredient")
            return redirect("recipe-edit", recipe_id)
        else:
            messages.warning(request, "Invalid data in ingredient")
            return redirect(
                "recipe_ingredients:ingredient-edit", recipe_id, ingredient_id
            )


class RecipeIngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = RecipeIngredients

    def get_success_url(self):
        recipe_id = self.kwargs.get("recipe_id")
        success_url = reverse("recipe-edit", kwargs={"recipe_id": recipe_id})

        return success_url

    def form_valid(self, form):
        messages.success(self.request, "Successfully removed ingredient")
        return super().form_valid(form)
