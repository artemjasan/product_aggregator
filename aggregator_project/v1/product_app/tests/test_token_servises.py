import pytest
import responses
import requests
from unittest import mock

from django.conf import settings

from v1.product_app.custom_exceptions import UnsupportedOffersMicroserviceResponseStatus
from v1.product_app.models import OffersMicroserviceToken
from v1.product_app.services import token_services

TEST_ACCESS_TOKEN = '64ed5030-f9a7-4ddd-a586-71c2164c4b63'


@pytest.mark.django_db
@pytest.mark.parametrize(
    "to_create, expected_result",
    [
        (True, True), (False, False)
    ]
)
def test_token_existence_verification(
        to_create: bool,
        expected_result: bool
):
    if to_create:
        OffersMicroserviceToken.objects.create(access_token=TEST_ACCESS_TOKEN)

    assert token_services.token_existence_verification() == expected_result


@responses.activate
@pytest.mark.django_db
def test_load_access_token_from_offers_microservice_success():
    responses.post(
        settings.BASE_OFFER_MICROSERVICE_API + settings.MICROSERVICE_AUTH_PATH,
        json={"access_token": TEST_ACCESS_TOKEN},
        status=201
    )
    access_token = token_services.load_access_token_from_offers_microservice()

    assert access_token == '64ed5030-f9a7-4ddd-a586-71c2164c4b63'


@responses.activate
@pytest.mark.django_db
@pytest.mark.parametrize(
    "status",
    [300, 400, 500]
)
def test_load_access_token_from_offers_microservice_with_diff_wrong_status(status: int):
    responses.post(
        settings.BASE_OFFER_MICROSERVICE_API + settings.MICROSERVICE_AUTH_PATH,
        json={"msg": 'error'},
        status=status
    )
    with pytest.raises(UnsupportedOffersMicroserviceResponseStatus):
        token_services.load_access_token_from_offers_microservice()


@pytest.mark.django_db
def test_load_access_token_from_offers_microservice_connection_exception():
    with mock.patch(
            "v1.product_app.services.token_services.load_access_token_from_offers_microservice",
            side_effect=requests.exceptions.ConnectionError
    ):
        with pytest.raises(requests.exceptions.ConnectionError):
            token_services.load_access_token_from_offers_microservice()


@pytest.mark.django_db
def test_get_offers_microservice():
    token_services.store_access_token(TEST_ACCESS_TOKEN)
    result = token_services.get_offers_microservice_header()

    assert 'Bearer' in result
    assert result['Bearer'] == TEST_ACCESS_TOKEN
