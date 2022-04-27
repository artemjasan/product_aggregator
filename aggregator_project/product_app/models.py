from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(max_length=512)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Offer(models.Model):
    price = models.PositiveIntegerField()
    items_in_stock = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.price.__str__() + self.items_in_stock.__str__()

    class Meta:
        ordering = ["-id"]


class OffersMicroserviceToken(models.Model):
    access_token = models.CharField(max_length=128)

    def __str__(self):
        return self.access_token
