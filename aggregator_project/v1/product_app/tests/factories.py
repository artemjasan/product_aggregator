import factory
from django.contrib.auth import get_user_model
from factory import fuzzy


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("user_name")
    email = factory.Faker("email")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "product_app.Product"

    name = factory.Sequence(lambda n: f"{n} Product")
    description = factory.Faker("text")


class OfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "product_app.Offer"

    external_ms_id = fuzzy.FuzzyInteger(1, 10000)
    price = fuzzy.FuzzyInteger(1, 10000)
    items_in_stock = fuzzy.FuzzyInteger(1, 100)
    product = factory.SubFactory(ProductFactory)
