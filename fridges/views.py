from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from .forms import NewIngredientForm
from .models import Fridge


class FridgesHomePageView(LoginRequiredMixin, View):
    template_name = "fridges/home.html"

    def get(self, request):
        user_fridge = Fridge.objects.filter(user=request.user.pk).order_by("id")
        context = {"title": "Fridge", "fridge": user_fridge}
        return render(request, self.template_name, context)


class FridgeAddPageView(LoginRequiredMixin, View):
    template_name = "fridges/fridge_form.html"

    def get(self, request):
        form = NewIngredientForm()
        context = {"title": "Add Ingredient", "form": form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = NewIngredientForm(request.POST)
        if form.is_valid():
            ingredient, created = Fridge.objects.get_or_create(
                name=request.POST.get("name"),
                quantity_type=request.POST.get("quantity_type"),
                user=request.user.profile,
                defaults={"quantity": request.POST.get("quantity")},
            )
            if not created:
                ingredient.quantity = str(
                    int(ingredient.quantity) + int(request.POST.get("quantity"))
                )
                ingredient.save()
            messages.success(request, "Zawartość lodówki została dodana")
            return redirect("fridges-home-page")


class IngredientEditPageView(LoginRequiredMixin, View):
    template_name = "fridges/fridge_form.html"

    def get(self, request, ingredient_id):
        ingredient = get_object_or_404(Fridge, pk=ingredient_id)
        context = {"ingredient": ingredient, "form": ingredient}
        return render(request, self.template_name, context)

    def post(self, request, ingredient_id):
        form = NewIngredientForm(request.POST)
        if form.is_valid():
            Fridge.objects.filter(id=ingredient_id).update(
                name=request.POST.get("name"),
                quantity=request.POST.get("quantity"),
                quantity_type=request.POST.get("quantity_type"),
            )
            messages.success(request, "Składnik został zaktualizowany")
            return redirect("fridges-home-page")


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Fridge
    success_url = reverse_lazy("fridges-home-page")

    def form_valid(self, form):
        messages.success(self.request, "Pomyślnie usunięto składnik")
        return super().form_valid(form)
