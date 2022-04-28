import logging

from celery import shared_task

from .services import offer_services, product_services

logger = logging.getLogger("background_tasks")


@shared_task
def create_or_update_product_offers() -> None:
    """
    Celery shared task which schedule deletes failed old temporary links.
    """
    logger.info("Starting the background task")
    if product_services.checking_for_product_existence():
        logger.info("Starting create or update product's offers")
        offer_services.create_or_update_product_offers()

