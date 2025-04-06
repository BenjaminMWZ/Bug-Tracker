import logging
from celery import shared_task
from django.core.management import call_command

logger = logging.getLogger('bug_tracker')

@shared_task
def process_emails_task():
    """
    Process unread bug report emails.
    This task calls the custom management command 'process_emails'.
    """
    try:
        logger.info("Starting scheduled email processing task")
        call_command('process_emails')
        logger.info("Email processing task completed successfully")
        return "Emails processed successfully"
    except Exception as e:
        logger.error(f"Error processing emails: {str(e)}")
        # Re-raise if you want Celery to mark the task as failed
        raise