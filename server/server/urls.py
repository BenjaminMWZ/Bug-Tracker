from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect

# Simple view to handle the root URL
def home(request):
    return HttpResponse("Welcome to Bug Tracker API. <a href='/api/'>Access API</a>")

# Alternative: redirect to API root
def redirect_to_api(request):
    return redirect('/api/')

urlpatterns = [
    path('', home, name='home'),  # Add this line for the root URL
    path('admin/', admin.site.urls),
    path('api/', include('issues.urls')),  # Prefix all issues URLs with /api/
]