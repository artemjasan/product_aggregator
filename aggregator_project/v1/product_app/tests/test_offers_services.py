from typing import Final

import pytest
import responses
import requests
from unittest import mock

from django.conf import settings
from rest_framework import status

from v1.product_app.custom_exceptions import (
    ErrorOffersMicroserviceResponseStatus, UnsupportedOffersMicroserviceResponseStatus
)
from v1.product_app.models import Offer
from v1.product_app.services import offer_services
from v1.product_app.services.offer_services import ERROR_RESPONSE_STATUS
from v1.product_app.tests.factories import ProductFactory


MOCKED_PRODUCT_ID: Final = 2
MOCKED_OFFERS_DATA: Final = (
    {"id": 100, "price": 10, "items_in_stock": 10},
    {"id": 200, "price": 20, "items_in_stock": 20}
)
MOCKED_OFFERS_DATA_UPDATED: Final = (
    {"id": 100, "price": 1000, "items_in_stock": 1000},
    {"id": 300, "price": 30, "items_in_stock": 30}
)
MOCKED_OFFERS_DATA_WRONG: Final = (
    {"id": 100, "price": 10, "items_in_stock": 10},
    {"id": 200, "price": -20, "items_in_stock": -20}
)


@responses.activate
@pytest.mark.django_db
def test_get_product_offers_success():
    responses.get(
        settings.BASE_OFFER_MICROSERVICE_API + f"/products/{MOCKED_PRODUCT_ID}" +
        settings.MICROSERVICE_GET_PRODUCT_OFFERS_PATH,
        json=MOCKED_OFFERS_DATA,
        status=status.HTTP_200_OK
    )
    response = offer_services.get_product_offers(MOCKED_PRODUCT_ID)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2

    for i, offer in enumerate(response.json()):
        assert offer.get("id") == MOCKED_OFFERS_DATA[i].get("id")
        assert offer.get("price") == MOCKED_OFFERS_DATA[i].get("price")
        assert offer.get("items_in_stock") == MOCKED_OFFERS_DATA[i].get("items_in_stock")


@responses.activate
@pytest.mark.django_db
@pytest.mark.parametrize("status_code", ERROR_RESPONSE_STATUS)
def test_get_product_offers_failed_error_response_status(status_code: int):
    responses.get(
        settings.BASE_OFFER_MICROSERVICE_API + f"/products/{MOCKED_PRODUCT_ID}" +
        settings.MICROSERVICE_GET_PRODUCT_OFFERS_PATH,
        json={"msg": 'error'},
        status=status_code
    )
    with pytest.raises(ErrorOffersMicroserviceResponseStatus):
        offer_services.get_product_offers(MOCKED_PRODUCT_ID)


@responses.activate
@pytest.mark.django_db
@pytest.mark.parametrize("status_code", [300, 500])
def test_get_product_offers_failed_error_unsupport_response_status(status_code: int):
    responses.get(
        settings.BASE_OFFER_MICROSERVICE_API + f"/products/{MOCKED_PRODUCT_ID}" +
        settings.MICROSERVICE_GET_PRODUCT_OFFERS_PATH,
        json={"msg": 'error'},
        status=status_code
    )
    with pytest.raises(UnsupportedOffersMicroserviceResponseStatus):
        offer_services.get_product_offers(MOCKED_PRODUCT_ID)


@pytest.mark.django_db
def test_get_product_offers_failed_connection_exception():
    with mock.patch(
            "v1.product_app.services.offer_services.get_product_offers",
            side_effect=requests.exceptions.ConnectionError
    ):
        with pytest.raises(requests.exceptions.ConnectionError):
            offer_services.get_product_offers(MOCKED_PRODUCT_ID)


@responses.activate
@pytest.mark.django_db
def test_create_or_update_product_offers_success(
        product_factory: ProductFactory
):
    product = product_factory.create(id=MOCKED_PRODUCT_ID)
    responses.get(
        settings.BASE_OFFER_MICROSERVICE_API + f"/products/{MOCKED_PRODUCT_ID}" +
        settings.MICROSERVICE_GET_PRODUCT_OFFERS_PATH,
        json=MOCKED_OFFERS_DATA,
        status=status.HTTP_200_OK
    )
    offer_services.create_product_offers()
    offers = Offer.objects.all().order_by('external_ms_id')

    for i, offer in enumerate(offers):
        assert offer.external_ms_id == MOCKED_OFFERS_DATA[i].get("id")
        assert offer.price == MOCKED_OFFERS_DATA[i].get("price")
        assert offer.items_in_stock == MOCKED_OFFERS_DATA[i].get("items_in_stock")
        assert offer.product.id == product.id


@responses.activate
@pytest.mark.django_db
def test_create_or_update_product_two_load_product_offers(
        product_factory: ProductFactory
):
    product = product_factory.create(id=MOCKED_PRODUCT_ID)
    responses.get(
        settings.BASE_OFFER_MICROSERVICE_API + f"/products/{MOCKED_PRODUCT_ID}" +
        settings.MICROSERVICE_GET_PRODUCT_OFFERS_PATH,
        json=MOCKED_OFFERS_DATA,
        status=status.HTTP_200_OK
    )
    offer_services.create_product_offers()
    responses.get(
        settings.BASE_OFFER_MICROSERVICE_API + f"/products/{MOCKED_PRODUCT_ID}" +
        settings.MICROSERVICE_GET_PRODUCT_OFFERS_PATH,
        json=MOCKED_OFFERS_DATA_UPDATED,
        status=status.HTTP_200_OK
    )
    offer_services.create_product_offers()
    offers = Offer.objects.all().order_by('external_ms_id')

    assert len(offers) == len(MOCKED_OFFERS_DATA_UPDATED)

    for i, offer in enumerate(offers):
        assert offer.external_ms_id == MOCKED_OFFERS_DATA_UPDATED[i].get("id")
        assert offer.price == MOCKED_OFFERS_DATA_UPDATED[i].get("price")
        assert offer.items_in_stock == MOCKED_OFFERS_DATA_UPDATED[i].get("items_in_stock")
        assert offer.product.id == product.id


@responses.activate
@pytest.mark.django_db
def test_create_or_update_product_offers_failed(
        product_factory: ProductFactory
):
    product_factory.create(id=MOCKED_PRODUCT_ID)
    responses.get(
        settings.BASE_OFFER_MICROSERVICE_API + f"/products/{MOCKED_PRODUCT_ID}" +
        settings.MICROSERVICE_GET_PRODUCT_OFFERS_PATH,
        json={"msg": 'error'},
        status=status.HTTP_400_BAD_REQUEST
    )
    with pytest.raises(ErrorOffersMicroserviceResponseStatus):
        offer_services.create_product_offers()

