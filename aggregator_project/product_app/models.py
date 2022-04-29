from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(max_length=512)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Offer(models.Model):
    external_ms_id = models.IntegerField(null=True)
    price = models.PositiveIntegerField()
    items_in_stock = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.external_ms_id)

    class Meta:
        ordering = ["-id"]


class OffersMicroserviceToken(models.Model):
    access_token = models.CharField(max_length=128)

    def __str__(self):
        return self.access_token