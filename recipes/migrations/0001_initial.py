# Generated by Django 4.2.5 on 2024-01-17 20:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
        ("recipe_ingredients", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("recipe_name", models.CharField(max_length=100, unique=True)),
                ("preparation", models.TextField(default="")),
                ("builtin", models.BooleanField(default=False)),
                ("public", models.BooleanField(default=True)),
                (
                    "recipe_ingredient",
                    models.ManyToManyField(to="recipe_ingredients.recipeingredient"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="users.profile",
                    ),
                ),
            ],
        ),
    ]
