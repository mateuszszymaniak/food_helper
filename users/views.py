from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import AuthenticationForm, LoginView, PasswordResetView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

from .forms import MyResetPasswordForm, UserRegisterForm


class CustomAuthForm(AuthenticationForm):
    error_messages = {"invalid_login": "Wrong email or password"}


class MyResetPasswordView(PasswordResetView):
    form_class = MyResetPasswordForm
    success_url = reverse_lazy("login-page")

    def form_valid(self, form):
        email = form.data.get("email")
        new_password = form.data.get("new_password")
        confirm_new_password = form.data.get("confirm_new_password")

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            messages.warning(self.request, "Email does not exist")
            return redirect("reset-password-page")

        if new_password == confirm_new_password:
            user.set_password(new_password)
            user.save()
            messages.success(self.request, "Password successfully reset.")
            return redirect("login-page")
        else:
            messages.error(self.request, "Passwords are not the same")
            return redirect("reset-password-page")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid form submission")
        return super().form_invalid(form)


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    form_class = CustomAuthForm
    success_url = reverse_lazy("users/home.html")


class HomePageView(LoginRequiredMixin, View):
    template_name = "users/home.html"
    context = {"title": "Home Page"}

    def get(self, request):
        if request.user.is_authenticated:
            user_ingredients = request.user.profile.useringredient_set.all()
            user_recipes = request.user.profile.recipe_set.all()
            ready_recipes, sorted_keys = self.ready_recipes(
                user_recipes, user_ingredients
            )
            self.context["ready_recipes"] = ready_recipes
            self.context["sorted_keys"] = sorted_keys
            self.template_name = "users/dashboard.html"
            return render(request, self.template_name, self.context)
        else:
            return render(request, self.template_name, self.context)

    def ready_recipes(self, user_recipes, user_ingredients):
        result_recipes = {}

        for recipe in user_recipes:
            ingredients = recipe.recipe_ingredient.all()
            if len(ingredients) == 0:
                continue
            missing_ingredients_counter = 0
            for ingredient_item in ingredients:
                ingredient_name = ingredient_item.ingredient.product.name
                ingredient_quantity = ingredient_item.amount
                ingredient_quantity_type = ingredient_item.ingredient.quantity_type
                ingredient_found = False
                for user_ingredient_item in user_ingredients:
                    if (
                        ingredient_name == user_ingredient_item.ingredients.product.name
                        and ingredient_quantity <= user_ingredient_item.amount
                        and ingredient_quantity_type
                        == user_ingredient_item.ingredients.quantity_type
                    ):
                        ingredient_found = True
                        break
                if not ingredient_found:
                    missing_ingredients_counter += 1
            if str(missing_ingredients_counter) in result_recipes:
                result_recipes[str(missing_ingredients_counter)].append(recipe)
            else:
                result_recipes[str(missing_ingredients_counter)] = [recipe]
        sorted_keys = sorted(result_recipes.keys())
        return result_recipes, sorted_keys


class RegisterView(View):
    template_name = "users/register.html"
    form = UserRegisterForm()
    context = {"title": "Register", "form": form}

    def get(self, request):
        return render(request, self.template_name, self.context)

    @staticmethod
    def post(request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email_in_db = User.objects.filter(email=form.data.get("email"))
            if not email_in_db:
                form.save()
                messages.success(request, "User created correctly")
                return redirect("login-page")
        messages.warning(request, "Form have invalid data")
        return redirect("register-page")


class ProfileView(View):
    template_name = "users/profile.html"
    context = {"title": "Profile"}

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name, self.context)
