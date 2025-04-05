"""
WSGI config for bug_tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys
# Now, remove the extra ".." so that project_root is Bug-Tracker/server.
project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
application = get_wsgi_application()