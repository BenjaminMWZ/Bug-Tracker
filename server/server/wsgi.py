import os
import sys

# Debug: Print information about the environment
print("Current directory:", os.getcwd())
print("Python path before:", sys.path)
print("Directory contents:", os.listdir(os.getcwd()))

# Add the parent directory to sys.path to help Python find the settings module
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)
print("Added to path:", base_dir)
print("Python path after:", sys.path)

from django.core.wsgi import get_wsgi_application 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
print("Settings module:", os.environ.get("DJANGO_SETTINGS_MODULE"))

application = get_wsgi_application()