from typing import Final

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .conftest import try_all_authentications_with_codes
from .factories import OfferFactory, ProductFactory

OFFER_DATA: Final = {"id": 100, "external_ms_id": 100, "price": 100, "items_in_stock": 100, "product": 1}


@pytest.mark.django_db
@pytest.mark.parametrize(**try_all_authentications_with_codes(401, 200, 200))
def test_get_offers_list_different_auths_status_code(
    offer_factory: OfferFactory, configured_api_client: APIClient, status_code: int
):
    offer_factory.create_batch(2)
    response = configured_api_client.get(reverse("offer-list"))

    assert response.status_code == status_code


@pytest.mark.django_db
def test_get_offers_list(
    offer_factory: OfferFactory,
    product_factory: ProductFactory,
    registered_api_client: APIClient,
):
    product = product_factory.create()
    offer_factory.create(product=product), offer_factory.create(product=product)
    response = registered_api_client.get(reverse("offer-list"))
    results = response.data["results"]

    assert response.status_code == status.HTTP_200_OK
    assert len(results) == 2
    for offer in results:
        assert "id" in offer
        assert "external_ms_id" in offer
        assert "price" in offer
        assert "items_in_stock" in offer
        assert "product" in offer


@pytest.mark.django_db
def test_get_offers_list_values(
    offer_factory: OfferFactory,
    product_factory: ProductFactory,
    registered_api_client: APIClient,
):
    product = product_factory.create()
    offer = offer_factory.create(product=product)

    response = registered_api_client.get(reverse("offer-list"))
    result = response.data["results"][0]

    assert response.status_code == status.HTTP_200_OK
    assert result.get("id") == offer.id
    assert result.get("external_ms_id") == offer.external_ms_id
    assert result.get("price") == offer.price
    assert result.get("items_in_stock") == offer.items_in_stock
    assert result.get("product") == offer.product.id


@pytest.mark.django_db
def test_get_offer_detail(
    registered_api_client: APIClient, product_factory: ProductFactory, offer_factory: OfferFactory
):
    product = product_factory.create()
    offer = offer_factory.create(product=product)
    response = registered_api_client.get(reverse("offer-detail", args=[offer.id]))
    assert response.status_code == status.HTTP_200_OK
    data = response.data

    assert data.get("id") == offer.id
    assert data.get("external_ms_id") == offer.external_ms_id
    assert data.get("price") == offer.price
    assert data.get("items_in_stock") == offer.items_in_stock
    assert data.get("product") == offer.product.id


@pytest.mark.django_db
def test_get_offer_detail_non_existing(
    registered_api_client: APIClient,
):
    response = registered_api_client.get(reverse("offer-detail", args=[123456789]))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(**try_all_authentications_with_codes(401, 400, 400))
def test_post_new_offer_different_auths(configured_api_client: APIClient, status_code: int):
    response = configured_api_client.post(reverse("product-list"), data=OFFER_DATA)

    assert response.status_code == status_code


@pytest.mark.django_db
def test_update_exists_offer(
    registered_api_client: APIClient, offer_factory: OfferFactory, product_factory: ProductFactory
):
    product = product_factory.create()
    offer = offer_factory.create()
    response = registered_api_client.put(
        reverse("offer-detail", args=[offer.id]),
        data={"external_ms_id": 100, "price": 999, "items_in_stock": 0, "product": product.id},
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_delete_exists_offer(registered_api_client: APIClient, offer_factory: OfferFactory):
    offer = offer_factory.create()
    response = registered_api_client.delete(reverse("offer-detail", args=[offer.id]))
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
