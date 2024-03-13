from django.apps import AppConfig


class RecipesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recipes"

    def ready(self):
        from .signals import pre_delete_recipe  # noqa: F401
