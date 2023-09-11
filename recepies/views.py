from django.shortcuts import render, redirect
from .forms import CreateNewRecepie, RecepieIngredientsForm  # , IngredientFormSet
from django.contrib import messages
from .models import Recepie
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required

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


@login_required
def recepies_add(request):
    if request.method == "POST":
        form = RecepieIngredientsForm(request.POST)
        if form.is_valid():
            recepie = form.save(commit=False)
            recepie.user_fk = request.user.profile
            recepie.save()
            messages.success(request, "Przepis został dodany")
            return redirect("recepies_home_page")
    else:
        form = RecepieIngredientsForm()
    return render(
        request, "recepies/recepie_form.html", {"title": "Add Recepie", "form": form}
    )
