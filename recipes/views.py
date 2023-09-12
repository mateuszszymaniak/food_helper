from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import RecipeIngredientsForm
from .models import Recipe


def recipes_home_page(request):
    user_recipes = Recipe.objects.all().filter(user_fk=request.user.pk)
    context = {"title": "Recipes", "recipes": user_recipes}

    return render(request, "recipes/home.html", context)


class RecipesHomePageView(View):
    template_name = "recipes/home.html"

    def get(self, request):
        user_recipes = Recipe.objects.all().filter(user_fk=request.user.pk)
        context = {"title": "Recipes", "recipes": user_recipes}

        return render(request, self.template_name, context)


class RecipeAddPageView(View):
    template_name = "recipes/recipe_form.html"

    @method_decorator(login_required)
    def get(self, request):
        form = RecipeIngredientsForm()
        context = {"title": "Add Recipe", "form": form}

        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        form = RecipeIngredientsForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user_fk = request.user.profile
            recipe.save()
            messages.success(request, "Przepis został dodany")
            return redirect("recipes_home_page")
