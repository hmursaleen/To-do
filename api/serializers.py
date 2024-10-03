from rest_framework import serializers
from tasks.models import Task


'''
ModelSerializer: We use ModelSerializer as it provides an easy way to create a serializer class based on a model.
Fields: The fields attribute lists all the model fields we want to expose in the API.
Read-only fields: We set id, owner, created_at, and updated_at as read-only because they shouldn't be modified directly via the API.
'''


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model to facilitate CRUD operations via API.
    """

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'owner', 'created_at', 
            'updated_at', 'due_date', 'priority', 'is_completed'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
