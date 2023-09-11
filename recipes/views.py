from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateNewRecipe, RecipeIngredientsForm  # , IngredientFormSet
from django.contrib import messages
from .models import Recipe
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required

# Create your views here.


def recipes_home_page(request):
    return render(
        request,
        "recipes/home.html",
        {
            "title": "Recipes",
            "recipes": Recipe.objects.all().filter(user_fk=request.user.pk),
        },
    )


@login_required
def recipes_add(request):
    if request.method == "POST":
        form = RecipeIngredientsForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user_fk = request.user.profile
            recipe.save()
            messages.success(request, "Przepis został dodany")
            return redirect("recipes_home_page")
    else:
        form = RecipeIngredientsForm()
    return render(
        request, "recipes/recipe_form.html", {"title": "Add Recipe", "form": form}
    )
