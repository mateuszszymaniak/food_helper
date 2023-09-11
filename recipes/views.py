from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateNewRecepie, RecepieIngredientsForm  # , IngredientFormSet
from django.contrib import messages
from .models import Recepie
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required

# Create your views here.


def recipes_home_page(request):
    return render(
        request,
        "recipes/home.html",
        {
            "title": "Recipes",
            "recipes": Recepie.objects.all().filter(user_fk=request.user.pk),
        },
    )


@login_required
def recipes_add(request):
    if request.method == "POST":
        form = RecepieIngredientsForm(request.POST)
        if form.is_valid():
            recepie = form.save(commit=False)
            recepie.user_fk = request.user.profile
            recepie.save()
            messages.success(request, "Przepis został dodany")
            return redirect("recipes_home_page")
    else:
        form = RecepieIngredientsForm()
    return render(
        request, "recipes/recepie_form.html", {"title": "Add Recepie", "form": form}
    )
