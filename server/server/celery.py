from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
# This ensures Celery knows which settings to use when running as a standalone process.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

# Create a Celery instance named 'server'
app = Celery('server')
app.conf.beat_max_loop_interval = 5  # Check for scheduled tasks every 5 seconds

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# The 'namespace' parameter prefixes Celery-specific settings with CELERY_ in settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# This automatically discovers tasks.py files in all app directories.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    """
    Simple debug task that prints the request object.
    
    This can be used for testing that Celery is working properly.
    The 'bind=True' parameter ensures that 'self' refers to the task instance.
    
    Args:
        self: The task instance (provided by bind=True decorator)
        
    Returns:
        None (prints request information to console)
    """
    print(f'Request: {self.request!r}')