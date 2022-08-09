from uuid import uuid4

from django.conf import settings
from django.db import models


class Distillery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)
    country = models.ForeignKey("world.Country", on_delete=models.CASCADE)
    region = models.ForeignKey("world.Region", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class CaskType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class SpiritType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class Bottle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)
    distillery = models.ForeignKey(Distillery, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    spirit_type = models.ForeignKey(SpiritType, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(null=True)
    distillation_date = models.DateTimeField(null=True)
    bottle_date = models.DateTimeField(null=True)
    abv = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


# class BottleCask(models.Model):
#     cask_type = models.ForeignKey("cask.CaskType")


class FlavorProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name
