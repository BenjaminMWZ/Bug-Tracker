# issues/views.py

from rest_framework import generics
from .models import Bug, BugModification
from .serializers import BugSerializer, BugModificationSerializer

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
class BugModificationListView(generics.ListAPIView):
    queryset = BugModification.objects.all()
    serializer_class = BugModificationSerializer