from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncDate
from .models import Bug
from .serializers import BugSerializer
from datetime import timedelta, date
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import logging
from django.http import HttpResponse
from django.shortcuts import render

# Add this function at the beginning or end of your views.py file
def home(request):
    """Simple view that returns the home page."""
    return HttpResponse("Bug Tracker")

# Custom pagination class (optional, for more control)
class BugPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow clients to specify page size
    max_page_size = 50  # Maximum number of items per page

# GET /api/bugs/
class BugListView(generics.ListAPIView):
    """
    API view that returns a paginated list of all bugs.
    
    This view handles GET requests to retrieve a list of all bug reports.
    Results are paginated using BugPagination class, and authentication is required.
    
    Endpoint: GET /api/bugs/
    Query parameters:
        page: Page number (default: 1)
        page_size: Number of items per page (default: 10, max: 50)
    """
    queryset = Bug.objects.all()  # Get all bug records
    serializer_class = BugSerializer  # Use BugSerializer for conversion to JSON
    pagination_class = BugPagination  # Enable pagination
    permission_classes = [IsAuthenticated]  # Require authentication


# GET /api/bugs/<bug_id>/
class BugDetailView(generics.RetrieveAPIView):
    """
    API view that returns details for a specific bug.
    
    This view handles GET requests to retrieve a single bug report 
    identified by its bug_id.
    
    Endpoint: GET /api/bugs/<bug_id>/
    URL parameters:
        bug_id: The unique identifier for the bug (e.g., BUG-1234)
    """
    queryset = Bug.objects.all()  # Get all bug records
    serializer_class = BugSerializer  # Use BugSerializer for conversion to JSON
    lookup_field = 'bug_id'  # This makes it match the custom bug_id instead of pk
    permission_classes = [IsAuthenticated]  # Require authentication

# Get a logger for the views
logger = logging.getLogger('bug_tracker')

#  GET /api/bug_modifications/
class BugModificationListView(APIView):
    """
    API view that returns aggregated bug modification data for charting.
    
    This view handles GET requests to retrieve counts of bug modifications
    grouped by date, intended for visualization in the dashboard.
    
    Endpoint: GET /api/bug_modifications/
    Returns:
        JSON array of objects with 'date' and 'count' fields, showing the
        number of bugs modified on each date over the past week.
    """
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for bug modification statistics.
        
        Aggregates bug records by date and counts modifications,
        providing data for the past 7 days.
        
        Args:
            request: The HTTP request object
            
        Returns:
            Response: JSON data with dates and modification counts
        """
        try:
            # Get today's date and calculate the date one week ago
            today = date.today()
            one_week_ago = today - timedelta(days=7)
            
            logger.info(f"Fetching bug modifications from {one_week_ago} to {today}")

            # Generate a list of dates for the past week
            default_dates = {str(one_week_ago + timedelta(days=i)): 0 for i in range(8)}

            # Aggregate Bug records by date and count the number of modifications
            aggregated_data = (
                Bug.objects.filter(modified_count__gt=0)  # Only include bugs that were modified
                .annotate(date=TruncDate('updated_at'))  # Truncate updated_at to date
                .values('date')  # Group by date
                .annotate(count=Count('id'))  # Count the number of bugs modified on each date
                .order_by('date')  # Order by date
            )

            # Update the default dates with actual modification counts
            for entry in aggregated_data:
                date_str = entry["date"].strftime("%Y-%m-%d")
                default_dates[date_str] = entry["count"]

            # Format the data as a list of dictionaries
            result = [{"date": date_str, "count": count} for date_str, count in default_dates.items()]
            
            return Response(result)
            
        except Exception as e:
            logger.error(f"Error fetching bug modifications: {str(e)}")
            return Response(
                {"error": "Failed to retrieve bug modifications data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )