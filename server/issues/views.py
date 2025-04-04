from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncDate
from .models import Bug
from .serializers import BugSerializer

# GET /api/bugs/
class BugListView(generics.ListAPIView):
    queryset = Bug.objects.all()
    serializer_class = BugSerializer


# GET /api/bugs/<bug_id>/
class BugDetailView(generics.RetrieveAPIView):
    queryset = Bug.objects.all()
    serializer_class = BugSerializer
    lookup_field = 'bug_id'  # This makes it match the custom bug_id instead of pk


# GET /api/bug_modifications/
class BugModificationListView(APIView):
    def get(self, request, *args, **kwargs):
        # Aggregate Bug records by date and count the number of modifications
        aggregated_data = (
            Bug.objects.filter(modified_count__gt=0)  # Only include bugs that were modified
            .annotate(date=TruncDate('updated_at'))  # Truncate updated_at to date
            .values('date')  # Group by date
            .annotate(count=Count('id'))  # Count the number of bugs modified on each date
            .order_by('date')  # Order by date
        )

        # Format the data as a list of dictionaries
        result = [{"date": entry["date"].strftime("%Y-%m-%d"), "count": entry["count"]} for entry in aggregated_data]

        return Response(result)