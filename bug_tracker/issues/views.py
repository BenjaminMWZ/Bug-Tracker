from rest_framework import generics
from .models import Bug
from .serializers import BugSerializer
from django.http import JsonResponse
from django.db.models import Count

# API View to list all bugs
class BugListView(generics.ListCreateAPIView):
    queryset = Bug.objects.all()
    serializer_class = BugSerializer

# API View to retrieve, update, or delete a specific bug
class BugDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bug.objects.all()
    serializer_class = BugSerializer

# Custom API View to show bug modification statistics
def bug_modifications_chart(request):
    data = Bug.objects.values('status').annotate(count=Count('status'))
    return JsonResponse(list(data), safe=False)