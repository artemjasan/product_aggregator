from django.apps import AppConfig


class ProductAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product_app'

    def ready(self):
        from .services import token_services

        if not token_services.token_existence_verification():
            token = token_services.load_access_token_from_offers_microservice()
            token_services.store_access_token(token)
