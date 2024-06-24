from django.db import models

from products.models import Product


class Ingredient(models.Model):
    AMOUNT_TYPE_CHOICES = (
        ("kg", "kg"),
        ("g", "g"),
        ("l", "l"),
        ("ml", "ml"),
        ("szt.", "szt."),
        ("opak.", "opak."),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_type = models.CharField(
        max_length=5,
        choices=AMOUNT_TYPE_CHOICES,
    )

    class Meta:
        unique_together = ["product", "quantity_type"]

    def __str__(self):
        return f"{self.product.name}, {self.quantity_type}"
