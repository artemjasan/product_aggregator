from urllib.error import HTTPError

from requests import post

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

from .token_services import get_offers_microservice_header
from ..models import Product


def product_registration(product_id: int) -> Response:
    """
    TODO: description
    :param product_id: id of the created product
    :return: Response
    """
    created_product = Product.objects.get(id=product_id)
    try:
        response = post(
            url=settings.BASE_OFFER_MICROSERVICE_API + settings.MICROSERVICE_REGISTRATION_PATH,
            data={'id': created_product.id, 'name': created_product.name, 'description': created_product.description},
            headers=get_offers_microservice_header()
        )
        if response.status_code != status.HTTP_201_CREATED:
            Product.objects.get(id=product_id).delete()

        return response
    # TODO: write correct way to except error if microservice doesn't work
    except HTTPError as error:
        raise error


def checking_for_product_existence():
    """
    Product service which checks product existence,
    :return: True if at least one product exists, otherwise False.
    """
    if Product.objects.all().count() > 0:
        return True
    return False

