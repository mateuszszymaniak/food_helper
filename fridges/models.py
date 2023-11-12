from django.db import models

from users.models import Profile


class Fridge(models.Model):
    AMOUNT_TYPE_CHOICES = (
        ("kg", "kg"),
        ("g", "g"),
        ("l", "l"),
        ("ml", "ml"),
        ("szt.", "szt."),
        ("opak.", "opak."),
    )

    name = models.CharField(max_length=50, blank=False)
    quantity = models.CharField(max_length=5, blank=False)
    quantity_type = models.CharField(
        max_length=5,
        choices=AMOUNT_TYPE_CHOICES,
        blank=False,
    )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="fridges")
