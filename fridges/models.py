from django.db import models

from users.models import Profile


# Create your models here.
class Fridge(models.Model):
    AMOUNT_TYPE_CHOICES = (
        ("kg", "kg"),
        ("g", "g"),
        ("l", "l"),
        ("ml", "ml"),
        ("szt.", "szt."),
        ("opak.", "opak."),
    )

    name = models.CharField(max_length=50, unique=True)
    quantity = models.CharField(max_length=5)
    quantity_type = models.CharField(
        max_length=5,
        choices=AMOUNT_TYPE_CHOICES,
    )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
