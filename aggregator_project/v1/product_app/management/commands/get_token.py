from django.core.management.base import BaseCommand

from v1.product_app.services import token_services


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Get access token command started."))

        if not token_services.token_existence_verification():
            token = token_services.load_access_token_from_offers_microservice()
            token_services.store_access_token(token)

            self.stdout.write(self.style.SUCCESS("Store the access token to DB."))

        self.stdout.write(self.style.SUCCESS("The access token is already exist in DB."))
