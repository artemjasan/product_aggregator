import requests

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

from .token_services import get_offers_microservice_header
from v1.product_app.models import Product


def product_registration(product_id: int) -> Response:
    """
    Product service which provides registration of the created product in Offers microservice,
    if response status code is 201, means that registration was successful and send data to view,
    otherwise product registration is failed and the service deletes the created product from local
    db and sends data to view. In the event of a network problem rise ConnectionError;
    :param product_id: id of the created product
    :return: Response
    """
    created_product = Product.objects.get(id=product_id)
    try:
        response = requests.post(
            url=settings.BASE_OFFER_MICROSERVICE_API + settings.MICROSERVICE_REGISTRATION_PATH,
            data={'id': created_product.id, 'name': created_product.name, 'description': created_product.description},
            headers=get_offers_microservice_header()
        )
        if response.status_code != status.HTTP_201_CREATED:
            Product.objects.get(id=product_id).delete()
        return response

    except requests.exceptions.ConnectionError:
        Product.objects.get(id=product_id).delete()
        raise requests.exceptions.ConnectionError("Failed to connect to Offers microservice!")


def checking_for_product_existence():
    """
    Product service which checks product existence,
    :return: True if at least one product exists, otherwise False.
    """
    if Product.objects.all().count() > 0:
        return True
    return False

