from django.shortcuts import render
from .forms import CreateNewRecepie, RecepieIngredientsForm  # , IngredientFormSet
from .models import Recepie

# Create your views here.


def recepies_home_page(request):
    return render(
        request,
        "recepies/home.html",
        {
            "title": "Recepies",
            "recepies": Recepie.objects.all().filter(user_fk=request.user.pk),
        },
    )


def recepies_add(request):
    if request.method == "POST":
        form = RecepieIngredientsForm(request.POST)
        if form.is_valid():
            recepie = form.save(commit=False)
            recepie.user_fk = request.user.profile
            recepie.save()
            pass
    else:
        form = RecepieIngredientsForm()
    return render(
        request, "recepies/recepie_add.html", {"title": "Add Recepie", "form": form}
    )

    """if request.method == "POST":
        form = IngredientFormSet(request.POST)
        if form.is_valid():
            x = 5
        pass
    else:
        form = CreateNewRecepie()
        ingredient_formset = IngredientFormSet()
    return render(request, "recepies/recepie_add.html", {'title': "Add Recepie", "form": form, "ingredient_formset": ingredient_formset})
    """
