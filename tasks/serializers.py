from rest_framework import serializers
from .models import Task

#serializers is to convert Python objects to JSON

class TaskInputSerialier(serializers.ModelSerializer):
    "Creates serialiers that is based on your Task model"
    "Modelsserializer a shortcut: it automatically knows the "
    "fields adn types from the model"
    "this serializer is to validte the input data"
    "Input validation only"
    class Meta:
        model = Task
        fields = ['title', 'completed']
        "It means only these two fields are allowed wn someone sends"
        "the data to create or update a task"
        "DRF will ignore any other fields the clents stries to send"


class TaskOutputSerializer(serializers.ModelSerializer):
    "Output shaping (e.g. add computed fields, hide sensitive data)"
    owner_username = serializers.CharField(source='owner.username',read_only=True)
    "We add a new field called owner username"
    "source = owner.usrname go to task's owner =>> get the username "
    "from it"
    "read_only = True ==>> client cannot send this field"
    ""
    class Meta:
        model = Task
        fields = ['id', 'title', 'completed', 'owner_username', 'created_at']
        "we will send back this data to the client "
        "other fields will not be sent"