from unittest import mock

import pytest

from django.urls import reverse
from rest_framework.test import APIClient

from .conftest import try_all_authentications_with_codes
from .factories import ProductFactory, OfferFactory

PRODUCT_DATA = {
    "name": "MacBook Air",
    "description": "some text"
}


@pytest.mark.django_db
@pytest.mark.parametrize(**try_all_authentications_with_codes(401, 200, 200))
def test_get_product_list_different_auths_status_code(
        product_factory: ProductFactory,
        configured_api_client: APIClient,
        status_code: int
):
    product_factory.create_batch(2)
    response = configured_api_client.get(reverse("product-list"))

    assert response.status_code == status_code


@pytest.mark.django_db
def test_get_product_list(
        product_factory: ProductFactory,
        registered_api_client: APIClient,
):
    product_factory.create_batch(2)
    response = registered_api_client.get(reverse("product-list"))
    results = response.data["results"]

    assert response.status_code == 200
    assert len(results) == 2
    for product in results:
        assert "id" in product
        assert "name" in product
        assert "description" in product
        assert "offers" in product


@pytest.mark.django_db
def test_get_new_product_max_limit(
        registered_api_client: APIClient,
        product_factory: ProductFactory
):
    product_factory.create_batch(15)
    response = registered_api_client.get(reverse("product-list"), data={"name": "Audi A4"})

    assert response.status_code == 200
    assert len(response.data["results"]) == 10


@pytest.mark.django_db
@pytest.mark.parametrize(**try_all_authentications_with_codes(401, 201, 201))
def test_post_new_product_different_auths(
        configured_api_client: APIClient,
        status_code: int
):
    with mock.patch("v1.product_app.services.product_services.product_registration"):
        response = configured_api_client.post(reverse("product-list"), data=PRODUCT_DATA)

    assert response.status_code == status_code


@pytest.mark.django_db
def test_post_new_post_without_description(
        registered_api_client: APIClient,
):
    with mock.patch("v1.product_app.services.product_services.product_registration"):
        response = registered_api_client.post(reverse("product-list"), data={"name": "Audi A4"})

    assert response.status_code == 400


@pytest.mark.django_db
def test_post_new_post_without_name(
        registered_api_client: APIClient,
):
    with mock.patch("v1.product_app.services.product_services.product_registration"):
        response = registered_api_client.post(reverse("product-list"), data={"description": "text"})

    assert response.status_code == 400


