from urllib.error import HTTPError
from requests import get
import logging

from django.conf import settings
from django.db import transaction

from rest_framework import status

from .token_services import get_offers_microservice_header
from ..custom_exceptions import WrongOffersMicroserviceResponseStatus, ClientErrorOffersMicroserviceResponseStatus
from ..models import Product, Offer

logger = logging.getLogger("offers_services")


def get_product_offers(product_id: int):
    """
    TODO: description
    :return:
    """
    try:
        response = get(
            url=settings.BASE_OFFER_MICROSERVICE_API + f"/products/{product_id}" +
                settings.MICROSERVICE_GET_PRODUCT_OFFERS_PATH,
            data={'id': product_id},
            headers=get_offers_microservice_header()
        )
        if response.status_code == status.HTTP_200_OK:
            return response
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            logger.error(f"Status: 400 BAD REQUEST, {response.json()}")
            raise ClientErrorOffersMicroserviceResponseStatus(response.status_code)
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            logger.error(f"Status: 401 UNAUTHORIZED, {response.json()}")
            raise ClientErrorOffersMicroserviceResponseStatus(response.status_code)
        else:
            logger.error(f"Status: Incorrect MS status, {response.json()}")
            raise WrongOffersMicroserviceResponseStatus(response.status_code)
    # TODO: write correct way to except error if microservice doesn't work
    except HTTPError as error:
        raise error


def create_or_update_product_offers():
    """
    TODO: description
    :return:
    """
    products = Product.objects.all()

    for product in products:
        product_offers = get_product_offers(product.id).json()
        logger.info(f"{product_offers}")
        product_offers_ids = []
        for product_offer in product_offers:

            with transaction.atomic():
                Offer.objects.update_or_create(
                    external_ms_id=product_offer.get("id"),
                    price=product_offer.get("price"),
                    items_in_stock=product_offer.get("items_in_stock"),
                    product=product,
                )
                product_offers_ids.append(product_offer.get("id"))

                # Delete not created and not updated product offers
                Offer.objects.filter(product=product.id).exclude(external_ms_id__in=product_offers_ids).delete()






