import logging
from typing import Final

import requests  # type: ignore
from django.conf import settings
from django.db import transaction
from rest_framework import status

from .token_services import get_offers_microservice_header
from v1.product_app.custom_exceptions import (
    ErrorOffersMicroserviceResponseStatus,
    UnsupportedOffersMicroserviceResponseStatus,
)
from v1.product_app.models import Offer, Product

logger = logging.getLogger("offers_services")

ERROR_RESPONSE_STATUS: Final = [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED, status.HTTP_404_NOT_FOUND]


def get_product_offers(product_id: int) -> requests.Response:
    """
    Offers service which provides to load product offers by using product id.
    if response status code is 200, means that load was successful, and send
    response with data.
    If response status code is in ERROR_RESPONSE_STATUS, write log and raise
    ErrorOffersMicroserviceResponseStatus custom exception.
    In the event of a network problem raise ConnectionError exception;
    :return: Response with data
    """
    try:
        response = requests.get(
            url=settings.BASE_OFFER_MICROSERVICE_API
            + f"/products/{product_id}"
            + settings.MICROSERVICE_GET_PRODUCT_OFFERS_PATH,
            data={"id": product_id},
            headers=get_offers_microservice_header(),
        )
        if response.status_code == status.HTTP_200_OK:
            return response
        elif response.status_code in ERROR_RESPONSE_STATUS:
            logger.error(f"Status: {response.status_code}, {response.json()}")
            raise ErrorOffersMicroserviceResponseStatus(response.status_code)
        else:
            logger.error(f"Status: Incorrect MS status, {response.json()}")
            raise UnsupportedOffersMicroserviceResponseStatus(response.status_code)
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError("Failed to connect to Offers microservice!")


def create_product_offers() -> None:
    """
    Offers service which provides form Offers microservice to load product offers,
    deletes previous instances and stores them in local db for each registered and stored product.
    """
    products = Product.objects.all()

    for product in products:
        product_offers = get_product_offers(product.id).json()
        Offer.objects.filter(product=product.id).delete()
        with transaction.atomic():
            Offer.objects.bulk_create(
                [
                    Offer.objects.create(
                        external_ms_id=product_offer.get("id"),
                        price=product_offer.get("price"),
                        items_in_stock=product_offer.get("items_in_stock"),
                        product=product,
                    )
                    for product_offer in product_offers
                ],
                ignore_conflicts=True,
            )
