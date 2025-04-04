from celery import shared_task
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_emails_task():
    logger.info("Started processing emails task")
    try:
        call_command('process_emails')
        logger.info("Successfully processed emails.")
    except Exception as e:
        logger.error(f"Error processing emails: {e}")