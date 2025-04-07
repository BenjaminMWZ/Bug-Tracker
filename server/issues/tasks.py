# 
# This file defines Celery tasks for the Bug Tracker application.
# Celery is used for asynchronous and scheduled processing of emails,
# allowing bug reports submitted via email to be automatically processed
# and added to the database without blocking the main application.

import logging
from celery import shared_task
from django.core.management import call_command

# Get logger instance for recording task execution information
logger = logging.getLogger('bug_tracker')

@shared_task
def process_emails_task():
    """
    Process unread bug report emails.
    This task calls the custom management command 'process_emails'.
    
    The task connects to the configured email server, fetches unread emails,
    parses them to extract bug information, and creates or updates bug records.
    
    Returns:
        str: Success message if emails were processed successfully
        
    Raises:
        Exception: Any exception that occurred during processing is re-raised
                   to ensure Celery marks the task as failed for proper monitoring
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