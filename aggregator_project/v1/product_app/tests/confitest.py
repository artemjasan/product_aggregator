from pytest_factoryboy import register

from . import factories


register(factories.UserFactory)
register(factories.ProductFactory)
register(factories.OfferFactory)
