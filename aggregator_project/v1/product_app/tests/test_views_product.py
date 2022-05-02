from typing import Final
from unittest import mock

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .conftest import try_all_authentications_with_codes
from .factories import ProductFactory

PRODUCT_DATA: Final = {"name": "MacBook Air", "description": "some text"}
UPDATED_PRODUCT_DATA: Final = {"name": "MacBook Air 128 GB", "description": "Some text about MacBook Air"}


@pytest.mark.django_db
@pytest.mark.parametrize(**try_all_authentications_with_codes(401, 200, 200))
def test_get_product_list_different_auths_status_code(
    product_factory: ProductFactory, configured_api_client: APIClient, status_code: int
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

    assert response.status_code == status.HTTP_200_OK
    assert len(results) == 2
    for product in results:
        assert "id" in product
        assert "name" in product
        assert "description" in product
        assert "offers" in product


@pytest.mark.django_db
def test_get_new_product_max_limit(registered_api_client: APIClient, product_factory: ProductFactory):
    product_factory.create_batch(15)
    response = registered_api_client.get(reverse("product-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 10


@pytest.mark.django_db
def test_get_product_detail(registered_api_client: APIClient, product_factory: ProductFactory):
    product = product_factory.create()
    response = registered_api_client.get(reverse("product-detail", args=[product.id]))

    assert response.status_code == status.HTTP_200_OK
    data = response.data

    assert data.get("id") == product.id
    assert data.get("name") == product.name
    assert data.get("description") == product.description
    assert data.get("offers") == list(product.offers.values())


@pytest.mark.django_db
def test_get_product_detail_non_existing(registered_api_client: APIClient, product_factory: ProductFactory):
    product_factory.create()
    response = registered_api_client.get(reverse("product-detail", args=[123456789]))

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(**try_all_authentications_with_codes(401, 201, 201))
def test_post_new_product_different_auths(configured_api_client: APIClient, status_code: int):
    with mock.patch("v1.product_app.services.product_services.product_registration"):
        response = configured_api_client.post(reverse("product-list"), data=PRODUCT_DATA)

    assert response.status_code == status_code


@pytest.mark.django_db
def test_post_new_post_without_description(
    registered_api_client: APIClient,
):
    with mock.patch("v1.product_app.services.product_services.product_registration"):
        response = registered_api_client.post(reverse("product-list"), data={"name": "Audi A4"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_post_new_post_without_name(
    registered_api_client: APIClient,
):
    with mock.patch("v1.product_app.services.product_services.product_registration"):
        response = registered_api_client.post(reverse("product-list"), data={"description": "text"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_exists_product(registered_api_client: APIClient, product_factory: ProductFactory):
    product = product_factory.create()
    with mock.patch("v1.product_app.services.product_services.product_registration"):
        response = registered_api_client.put(reverse("product-detail", args=[product.id]), data=UPDATED_PRODUCT_DATA)
    assert response.status_code == status.HTTP_200_OK
    data = response.data

    assert data.get("name") == UPDATED_PRODUCT_DATA.get("name")
    assert data.get("description") == UPDATED_PRODUCT_DATA.get("description")


@pytest.mark.django_db
def test_delete_product(registered_api_client: APIClient, product_factory: ProductFactory):
    product = product_factory.create()
    with mock.patch("v1.product_app.services.product_services.product_registration"):
        response = registered_api_client.delete(reverse("product-detail", args=[product.id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
