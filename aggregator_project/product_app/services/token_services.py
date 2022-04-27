from typing import Optional

import requests

from urllib.parse import urlsplit

from django.conf import settings

# from rest_framework.response import Response

from ..models import OffersMicroserviceToken


def token_existence_verification() -> bool:
    """
    Simple token service which provides checking access token in db,
    :return: result of check
    """
    return OffersMicroserviceToken.objects.all().exists()


def store_access_token(token: str) -> None:
    """
    TODO: description
    :param token: access token from Offers Microservice
    :return:
    """
    token = OffersMicroserviceToken(access_token=token)
    token.save()


def get_access_token() -> Optional[OffersMicroserviceToken]:
    """
    Simple token service, which allows to get first instance if possible, otherwise return None
    TODO: description
    :return: None or first instance
    """
    return OffersMicroserviceToken.objects.first()
