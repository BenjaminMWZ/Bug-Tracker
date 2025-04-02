from rest_framework import serializers
from .models import Bug

# This file defines the serializers for the bug tracking system.
# Serializers are used to convert complex data types, such as querysets and model instances, into native Python datatypes.
# The BugSerializer class is a ModelSerializer that automatically generates fields based on the Bug model.
# It includes all fields from the Bug model and is used for both serialization and deserialization of Bug instances.
class BugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bug
        fields = '__all__'