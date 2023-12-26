from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ProductForm
from .models import Product


class ProductHomePageView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "products/home.html"
    extra_context = {"title": "Products"}

    def get(self, request, *args, **kwargs):
        context = self.extra_context
        context["products"] = self.model.objects.all().order_by("id")
        return render(request, self.template_name, context)


class ProductAddPageView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    extra_context = {"title": "Add Product"}

    def get(self, request, *args, **kwargs):
        context = self.extra_context
        context["form"] = self.form_class
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            product = form.save()
            product_id = product.id
            messages.success(request, "Product has beed added")
            if kwargs.get("ingredient_id"):
                recipe_id = kwargs.get("recipe_id")
                ingredient_id = kwargs.get("ingredient_id")
                return redirect(
                    "ingredients:ingredient-edit", recipe_id, ingredient_id, product_id
                )
            if kwargs.get("recipe_id"):
                recipe_id = kwargs.get("recipe_id")
                return redirect(
                    "recipe_ingredients:ingredient-add", recipe_id, product_id
                )
            if kwargs.get("new"):
                return redirect("my_ingredients:useringredient-add", product_id)
            if kwargs.get("my_ingredient_id"):
                my_ingredient_id = kwargs.get("my_ingredient_id")
                return redirect(
                    "my_ingredients:useringredient-edit", my_ingredient_id, product_id
                )
            return redirect("products:products-home-page")
        else:
            messages.warning(request, "Invalid data in product")
            return redirect("products:product-add")


class ProductEditPageView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    extra_context = {"title": "Edit Product"}

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        product = get_object_or_404(self.model, pk=product_id)
        context = self.extra_context
        context["form"] = product
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        form = self.form_class(request.POST)
        if form.is_valid():
            self.model.objects.filter(id=product_id).update(
                name=form.cleaned_data.get("name")
            )
            messages.success(request, "Successfully edited product")
            return redirect("products:products-home-page")
        else:
            messages.warning(request, "Invalid data in product")
            return redirect("products:product-edit", product_id)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product

    def get_success_url(self):
        success_url = reverse("products:products-home-page")
        return success_url

    def form_valid(self, form):
        messages.success(self.request, "Successfully removed product")
        return super().form_valid(form)
