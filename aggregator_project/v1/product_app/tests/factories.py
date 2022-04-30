import factory

from factory import fuzzy
from django.contrib.auth import get_user_model

from v1.product_app import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("user_name")
    email = factory.Faker("email")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Product

    name = factory.Sequence(lambda n: f"{n} Product")
    description = factory.Faker("text")


class OfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Offer

    external_ms_id__in = fuzzy.FuzzyInteger(1, 10000)
    price = fuzzy.FuzzyInteger(1, 10000)
    items_in_stock = fuzzy.FuzzyInteger(1, 100)
    product = factory.SubFactory(ProductFactory)
