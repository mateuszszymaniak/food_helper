from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import NewIngredientForm
from .models import Fridge


class FridgesHomePageView(View):
    template_name = "fridges/home.html"

    @method_decorator(login_required)
    def get(self, request):
        user_fridge = Fridge.objects.all().filter(user=request.user.pk).order_by("id")
        context = {"title": "Fridge", "fridge": user_fridge}
        return render(request, self.template_name, context)


class FridgeAddPageView(View):
    template_name = "fridges/fridge_form.html"

    @method_decorator(login_required)
    def get(self, request):
        context = {"title": "Add Ingredient"}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        form = request.POST
        ingredients_list = list(filter(lambda key: key.startswith("quantity-"), form))
        for prefix in ingredients_list:
            quantity = form.get(prefix)
            name = form.get(f"{prefix.replace('quantity', 'name')}")
            quantity_type = form.get(f"{prefix.replace('quantity', 'quantity_type')}")
            try:
                ingredient = Fridge.objects.get(
                    name=name, quantity_type=quantity_type, user=request.user.profile
                )
                ingredient.quantity = int(ingredient.quantity) + int(quantity)
                ingredient.save()
            except Fridge.DoesNotExist:
                Fridge.objects.create(
                    name=name,
                    quantity=quantity,
                    quantity_type=quantity_type,
                    user=request.user.profile,
                )

            # if ingredient:
            #     pass
            # else:
            #     Fridge.objects.create(name=name, quantity=quantity, quantity_type=quantity_type)
        messages.success(request, "Zawartość lodówki została dodana")
        return redirect("fridges-home-page")


class IngredientEditPageView(View):
    template_name = "fridges/fridge_form.html"

    def get(self, request, ingredient_id):
        ingredient = get_object_or_404(Fridge, pk=ingredient_id)
        context = {"ingredient": ingredient}
        return render(request, self.template_name, context)

    def post(self, request, ingredient_id):
        ingredient = Fridge.objects.get(id=ingredient_id)
        ingredient.quantity = request.POST.get("quantity-0")
        ingredient.quantity_type = request.POST.get("quantity_type-0")
        ingredient.name = request.POST.get("name-0")
        ingredient.save()
        messages.success(request, "Składnik został zaktualizowany")
        return redirect("fridges-home-page")


class IngredientDeletePageView(View):
    def get(self, request, ingredient_id):
        self.post(request, ingredient_id)
        messages.success(request, "Pomyślnie usunięto składnik")
        return redirect("fridges-home-page")

    def post(self, request, ingredient_id):
        ingredient = get_object_or_404(Fridge, pk=ingredient_id)
        ingredient.delete()
