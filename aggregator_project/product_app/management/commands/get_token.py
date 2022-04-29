import logging

from django.core.management.base import BaseCommand

from product_app.services import token_services


logger = logging.getLogger("custom_command_get_access_token")


class Command(BaseCommand):

    def handle(self, *args, **options):
        logger.info("Starting get access token command")

        if not token_services.token_existence_verification():
            token = token_services.load_access_token_from_offers_microservice()
            token_services.store_access_token(token)
            logger.info("Store access token to DB")

        logger.info("Access token is already exist in DB")
