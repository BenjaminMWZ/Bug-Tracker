from rest_framework import serializers
from .models import Bug, BugModification

class BugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bug
        fields = '__all__'

class BugModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugModification
        fields = '__all__'