from typing import Optional
from requests import post
from urllib.error import HTTPError

from django.conf import settings
from rest_framework import status

from v1.product_app.models import OffersMicroserviceToken
from v1.product_app.custom_exceptions import WrongOffersMicroserviceResponseStatus


def token_existence_verification() -> bool:
    """
    Token service which provides checking existence at least ones token in db,
    :return: result of check
    """
    return OffersMicroserviceToken.objects.all().exists()


def store_access_token(token: str) -> None:
    """
    Token service, which
    :param token: access token from Offers Microservice
    :return: None
    """
    token = OffersMicroserviceToken(access_token=token)
    token.save()


def get_access_token() -> Optional[OffersMicroserviceToken]:
    """
    Token service, which allows to get last instance if possible, otherwise return None
    :return: None or last instance
    """
    return OffersMicroserviceToken.objects.last()


def load_access_token_from_offers_microservice() -> str:
    """
    Token service, which allows by POST request to the microservice,
    get access token, parse json and get it.
    If response status code does not 201 - created, raise exception,
    :return: access token in str format
    """
    try:
        response = post(
            url=settings.BASE_OFFER_MICROSERVICE_API + settings.MICROSERVICE_AUTH_PATH
        )
        if response.status_code == status.HTTP_201_CREATED:
            return response.json()["access_token"]
        else:
            raise WrongOffersMicroserviceResponseStatus(response.status_code)

    # TODO: write correct way to except error if microservice doesn't work
    except HTTPError as error:
        raise error


def get_offers_microservice_header():
    """
    Provides Bearer header with access token
    :return: bearer header
    """
    return {
        'Bearer': str(get_access_token())
    }

