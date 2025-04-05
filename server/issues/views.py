from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncDate
from .models import Bug
from .serializers import BugSerializer
from datetime import timedelta, date

# GET /api/bugs/
class BugListView(generics.ListAPIView):
    queryset = Bug.objects.all()
    serializer_class = BugSerializer


# GET /api/bugs/<bug_id>/
class BugDetailView(generics.RetrieveAPIView):
    queryset = Bug.objects.all()
    serializer_class = BugSerializer
    lookup_field = 'bug_id'  # This makes it match the custom bug_id instead of pk


#  GET /api/bug_modifications/
class BugModificationListView(APIView):
    def get(self, request, *args, **kwargs):
        # Get today's date and calculate the date one week ago
        today = date.today()
        one_week_ago = today - timedelta(days=7)

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