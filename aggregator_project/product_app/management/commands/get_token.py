from django.core.management.base import BaseCommand

from aggregator_project.product_app.services import token_services


class GetToken(BaseCommand):

    def handle(self, *args, **options):

        if not token_services.token_existence_verification():
            token = token_services.load_access_token_from_offers_microservice()
            token_services.store_access_token(token)
            self.stdout.write(self.style.SUCCESS('Get token'))
        self.stdout.write(self.style.SUCCESS('Start command'))
