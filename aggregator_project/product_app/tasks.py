import logging

from celery import shared_task

logger = logging.getLogger("product_tasks")


@shared_task
def delete_old_failed_temporary_links() -> None:
    """
    Celery shared task which schedule deletes failed old temporary links.
    """
    logger.info("Starting create and validate links")
    print("This is schedule task")
