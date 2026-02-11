from rest_framework import serializers
from .models import Task

class TaskInputSerialier(serializers.ModelSerializer):
    "Input validation only"
    class Meta:
        model = Task
        fields = ['title', 'completed']

class TaskOutputSerializer(serializers.ModelSerializer):
    "Output shaping (e.g. add computed fields, hide sensitive data)"
    owner_username = serializers.CharField(source='owner.username',read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'completed', 'owner_username', 'created_at']
        