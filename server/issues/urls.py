"""
URL configuration for bug_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import BugListView, BugDetailView, bug_modifications_chart

urlpatterns = [
    path('api/bugs/', BugListView.as_view(), name='bug-list'),
    path('api/bugs/<str:bug_id>/', BugDetailView.as_view(), name='bug-detail'),
    path('api/bug_modifications/', bug_modifications_chart, name='bug-modifications'),
]
