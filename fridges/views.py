from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import NewIngredientForm
from .models import Fridge


def recalculate_quantity(quantity_from_db, quantity_from_form):
    result = int(quantity_from_db) + int(quantity_from_form)
    return str(result)


class FridgesHomePageView(LoginRequiredMixin, ListView):
    model = Fridge
    template_name = "fridges/home.html"
    extra_context = {"title": "Fridge"}

    def get(self, request, *args, **kwargs):
        user_fridge = self.model.objects.filter(user=request.user.pk).order_by("id")
        context = self.extra_context
        context["fridge"] = user_fridge
        return render(request, self.template_name, context)


class FridgeAddPageView(LoginRequiredMixin, CreateView, UpdateView):
    model = Fridge
    form_class = NewIngredientForm
    template_name = "fridges/fridge_form.html"
    extra_context = {"title": "Add Fridge Ingredient"}

    def get(self, request, *args, **kwargs):
        context = self.extra_context
        context["form"] = self.form_class
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            ingredient, created = self.model.objects.get_or_create(
                name=form.cleaned_data.get("name"),
                quantity_type=form.cleaned_data.get("quantity_type"),
                user=request.user.profile,
                defaults={"quantity": form.cleaned_data.get("quantity")},
            )
            if not created:
                ingredient.quantity = recalculate_quantity(
                    ingredient.quantity, form.cleaned_data.get("quantity")
                )
                ingredient.save()
            messages.success(request, "Ingredient has been added to fridge")
            return redirect("fridges-home-page")
        else:
            messages.warning(request, "Invalid data in ingredient")
            return redirect("fridge-add")


class IngredientEditPageView(LoginRequiredMixin, UpdateView, DeleteView):
    model = Fridge
    form_class = NewIngredientForm
    template_name = "fridges/fridge_form.html"
    extra_context = {"title": "Edit Fridge Ingredient"}

    def get(self, request, *args, **kwargs):
        ingredient = get_object_or_404(self.model, pk=kwargs.get("ingredient_id"))
        context = self.extra_context
        context["form"] = ingredient
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        ingredient_id = kwargs.get("ingredient_id")
        form = self.form_class(request.POST)
        if form.is_valid():
            check_existing_ingredient = self.model.objects.filter(
                Q(name=form.cleaned_data.get("name"))
                & Q(quantity_type=form.cleaned_data.get("quantity_type"))
            ).first()
            if check_existing_ingredient:
                check_existing_ingredient.quantity = recalculate_quantity(
                    check_existing_ingredient.quantity,
                    form.cleaned_data.get("quantity"),
                )
                check_existing_ingredient.save()
                self.model.objects.get(id=ingredient_id).delete()
            else:
                self.model.objects.filter(id=ingredient_id).update(
                    name=form.cleaned_data.get("name"),
                    quantity=form.cleaned_data.get("quantity"),
                    quantity_type=form.cleaned_data.get("quantity_type"),
                )
            messages.success(request, "Ingredient has been updated")
            return redirect("fridges-home-page")
        else:
            messages.warning(request, "Invalid data in ingredient")
            return redirect("fridge-edit", ingredient_id)


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Fridge
    success_url = reverse_lazy("fridges-home-page")

    def form_valid(self, form):
        messages.success(self.request, "Successfully removed ingredient")
        return super().form_valid(form)
