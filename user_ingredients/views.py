from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ingredients.forms import IngredientsForm
from ingredients.models import Ingredient
from products.models import Product

from .models import UserIngredient


def delete_my_session(request):
    del request.session["product_id"]
    # if request.session["my_ingredient"]:
    #     del request.session["my_ingredient"]
    if request.session["my_ingredient_id"]:
        del request.session["my_ingredient_id"]


class UserIngredientsHomePageView(LoginRequiredMixin, ListView):
    model = UserIngredient
    template_name = "useringredients/home.html"
    extra_context = {"title": "My Ingredients"}

    def get(self, request, *args, **kwargs):
        context = self.extra_context
        context["useringredients"] = self.model.objects.filter(
            user=request.user.profile.id
        )
        return render(request, self.template_name, context)


class UserIngredientsAddPageView(LoginRequiredMixin, CreateView):
    model = UserIngredient
    form_class = IngredientsForm
    template_name = "useringredients/ingredient_form.html"
    extra_context = {"title": "Add My Ingredient"}

    def get(self, request, *args, **kwargs):
        context = self.extra_context
        # context["form"] = self.form_class
        if request.session.get("product_id"):
            product_id = request.session.get("product_id")
            context["form"] = self.form_class(initial={"product_name": product_id})
            del request.session["product_id"]
        else:
            context["form"] = self.form_class
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            if "add_product" in request.POST:
                request.session["my_ingredient"] = "my_ingredient"
                return redirect("products:product-add")
            ingredient, created = Ingredient.objects.get_or_create(
                product=form.cleaned_data.get("product_name"),
                amount=form.cleaned_data.get("amount"),
                quantity_type=form.cleaned_data.get("quantity_type"),
            )
            x = 5
            # ingredient = form.save(commit=False)
            # ingredient.product = form.cleaned_data.get("product_name")
            # ingredient.save()
            self.model.objects.get_or_create(
                user=request.user.profile,
                ingredients=ingredient,
                amount=ingredient.amount,
            )
            # useringredient.ingredients.add(ingredient)
            # request.user.profile.ingredients.add(useringredient)
            messages.success(request, "My Ingredient has been successfully added")
            return redirect("my_ingredients:useringredients-home-page")
        else:
            messages.warning(request, "Invalid data in my ingredients")
            return redirect("my_ingredients:useringredient-add")


class UserIngredientsEditPageView(LoginRequiredMixin, UpdateView):
    model = UserIngredient
    form_class = IngredientsForm
    template_name = "useringredients/ingredient_form.html"
    extra_context = {"title": "Edit My Ingredient"}

    def get(self, request, *args, **kwargs):
        # request.session.clear()
        my_ingredient_id = kwargs.get("my_ingredient_id")
        my_ingredient = get_object_or_404(self.model, pk=my_ingredient_id)
        context = self.extra_context
        if request.session.get("product_id"):
            product_id = request.session.get("product_id")
            my_ingredient.ingredients.product = Product.objects.get(id=product_id)
            delete_my_session(request)
        context["form"] = my_ingredient
        context["products"] = Product.objects.all()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        my_ingredient_id = kwargs.get("my_ingredient_id")
        form = self.form_class(request.POST)
        if form.is_valid():
            if "add_product" in request.POST:
                request.session["my_ingredient_id"] = my_ingredient_id
                # request.session["my_ingredient"] = "my_ingredient"
                return redirect("products:product-add")
            else:
                ingredient = form.save(commit=False)
                ingredient.product = ingredient.product = form.cleaned_data.get(
                    "product_name"
                )
                ingredient.save()
                self.model.objects.filter(id=my_ingredient_id).update(
                    ingredients=ingredient, amount=ingredient.amount
                )
                messages.success(request, "Successfully edited my ingredient")
                return redirect("my_ingredients:useringredients-home-page")
        else:
            messages.warning(request, "Invalid data in editing my ingredient")
            return redirect("my_ingredients:useringredient-edit", my_ingredient_id)


class UserIngredientsDeletePageView(LoginRequiredMixin, DeleteView):
    model = UserIngredient

    def get_success_url(self):
        success_url = reverse("my_ingredients:useringredients-home-page")
        return success_url

    def form_valid(self, form):
        messages.success(self.request, "Successfully removed my ingredient")
        return super().form_valid(form)
