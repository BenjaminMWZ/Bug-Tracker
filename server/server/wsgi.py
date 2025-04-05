import os
import sys

# Debug: Print environment information
print("========== DEBUG START ==========")
print("Current directory:", os.getcwd())
print("Python path before:", sys.path)
print("Directory contents:", os.listdir(os.getcwd()))

# Try multiple path configurations
server_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(server_dir)
project_root = os.path.dirname(base_dir)

# Add both server and base directory to the path
sys.path.insert(0, server_dir)
sys.path.insert(0, base_dir)

# If we're on Heroku, the structure is likely /app/server/...
if os.path.exists('/app'):
    sys.path.insert(0, '/app')

print("Added to path:", server_dir)
print("Added to path:", base_dir)
print("Python path after:", sys.path)
print("========== DEBUG END ==========")

# Set up the settings module before importing Django components
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
print("Settings module:", os.environ.get("DJANGO_SETTINGS_MODULE"))

# Now import Django components
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()