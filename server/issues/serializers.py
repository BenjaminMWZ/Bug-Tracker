from rest_framework import serializers
from .models import Bug

class BugSerializer(serializers.ModelSerializer):
    """
    Serializer for the Bug model.
    
    Converts Bug model instances to JSON for API responses and validates
    incoming data for creating or updating Bug records.
    
    This serializer includes all fields from the Bug model, providing a complete
    representation of bug data for the API.
    """
    class Meta:
        model = Bug
        fields = '__all__'


class BugModificationSerializer(serializers.Serializer):
    """
    Serializer for bug modification statistics.
    
    Used for the dashboard chart data endpoint that shows bug modifications over time.
    This is not tied to a specific model, but rather represents aggregated data.
    
    Contains two fields:
    - date: The date of modifications
    - count: The number of bugs modified on that date
    """
    date = serializers.DateField()
    count = serializers.IntegerField()