"""
URL Configuration for the Bug Tracker server project. server project.

This module defines the top-level URL routing for the entire Django application.
It maps URL patterns to views or includes URL patterns from other apps.

The urlpatterns list routes URLs to views. For more information:
https://docs.djangoproject.com/en/dev/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin interface accessible at /admin/
    path('api/', include('issues.urls')),  # Prefix all issues URLs with /api/
]