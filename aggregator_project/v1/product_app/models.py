from django.db import models


class ProductManager(models.Manager):
    """
    Prefetches info about offers for selected products.
    """

    def get_queryset(self):
        return super().get_queryset().prefetch_related("offers")


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=511)

    objects = models.Manager()
    offered_objects = ProductManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Offer(models.Model):
    external_ms_id = models.IntegerField()
    price = models.PositiveIntegerField()
    items_in_stock = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="offers")

    def __str__(self):
        return str(self.external_ms_id)

    class Meta:
        ordering = ["-id"]


class OffersMicroserviceToken(models.Model):
    access_token = models.CharField(max_length=128)

    def __str__(self):
        return self.access_token
