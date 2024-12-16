from django.db import models
from uuid import uuid4


class ProductType(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid4())
    name = models.CharField(max_length=300, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


# class Product(models.Model):
#     pass


# class Cart(models.Model):
#     pass


# class Order(models.Model):
#     pass


# class Promos(models.Model):
#     pass
