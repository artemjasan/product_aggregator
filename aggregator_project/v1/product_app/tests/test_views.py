import pytest

from django.urls import reverse
from rest_framework.test import APIClient

from confitest import try_all_authentications_with_codes
from v1.product_app.tests.factories import ProductFactory


@pytest.mark.django_db
@pytest.mark.parametrize(**try_all_authentications_with_codes(400, 200, 200))
def test_get_product_list(
        product_factory: type[ProductFactory],
        configured_api_client: APIClient,
        status_code: int
):
    product_factory.create_batch(2)
    response = configured_api_client.get(reverse("product-list"))
    results = response.data["results"]
    assert len(results) == 2
    for product in results:
        assert "id" in product
        assert "name" in product
        assert "description" in product
