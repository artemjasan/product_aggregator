# This import is required to ensure that the Celery app is loaded when Django starts
from .celery_app import app as celery_app
