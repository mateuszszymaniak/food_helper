from django.contrib.postgres.fields import ArrayField, HStoreField
from django.db import models
from users.models import Profile
from django.contrib.postgres.operations import HStoreExtension


# Create your models here.
class Recepie(models.Model):
    recepie_name = models.CharField(max_length=100)
    ingredients = models.JSONField()
    preparation = models.TextField(blank=False, default="")
    tags = ArrayField(models.CharField(max_length=20, null=True), blank=True, null=True)
    user_fk = models.ForeignKey(Profile, on_delete=models.CASCADE)
