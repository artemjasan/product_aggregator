import pytest as pytest
import responses

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from v1.product_app.custom_exceptions import WrongOffersMicroserviceResponseStatus
from v1.product_app.models import Product
from v1.product_app.tests.factories import ProductFactory
from v1.product_app.services import product_services


@responses.activate
@pytest.mark.django_db
def test_product_registration_success(
        product_factory: ProductFactory
):
    product = product_factory.create()
    responses.post(
        settings.BASE_OFFER_MICROSERVICE_API + settings.MICROSERVICE_REGISTRATION_PATH,
        json={"id": product.id},
        status=201
    )
    response = product_services.product_registration(product.id)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["id"] == product.id

    product_from_db = Product.objects.get(id=product.id)
    assert product_from_db.id == product.id


class InegrityError:
    pass


@responses.activate
@pytest.mark.django_db
def test_product_registration_failed(
        product_factory: ProductFactory
):
    product = product_factory.create()
    responses.post(
        settings.BASE_OFFER_MICROSERVICE_API + settings.MICROSERVICE_REGISTRATION_PATH,
        json={"code": "BAD_REQUEST", "msg": "It was bad request"},
        status=400
    )
    response = product_services.product_registration(product.id)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["code"] == "BAD_REQUEST"
    assert response.json()["msg"] == "It was bad request"
    
    with pytest.raises(ObjectDoesNotExist):
        Product.objects.get(id=product.id)
