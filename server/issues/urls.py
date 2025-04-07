from django.urls import path
from django.contrib import admin
from django.http import HttpResponse
from . import views
from .auth import LoginView, RegistrationView, UserProfileView

# Define a simple view for the root path
def home(request):
    return HttpResponse("Welcome to the Bug Tracker API. Use /bugs/ or /bug_modifications/.")

urlpatterns = [
    path('', home, name='home'),  # Root path
    path('admin/', admin.site.urls),
    path('api/bugs/', views.BugListView.as_view(), name='bug-list'),  # List all bugs
    path('api/bugs/<str:bug_id>/', views.BugDetailView.as_view(), name='bug-detail'),  # View specific bug
    path('api/bug_modifications/', views.BugModificationListView.as_view(), name='bug-modifications'),  # Aggregated bug modifications
    
    # Authentication endpoints
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/register/', RegistrationView.as_view(), name='register'),
    path('api/auth/profile/', UserProfileView.as_view(), name='profile'),

    # Home page
    path('', views.home, name='home'),
]