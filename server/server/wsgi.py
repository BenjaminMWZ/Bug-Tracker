import os
import sys

# Add the parent directory to sys.path to help Python find the settings module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.core.wsgi import get_wsgi_application 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings") 
application = get_wsgi_application()