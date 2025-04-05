import os
import sys
from pathlib import Path

# Get the current file's directory
current_dir = Path(__file__).resolve().parent
settings_path = current_dir.parent

# Make sure the settings directory is in the Python path
if str(settings_path) not in sys.path:
    sys.path.insert(0, str(settings_path))

# Set settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

# Import Django's WSGI application after path setup
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()