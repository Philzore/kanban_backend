from .models import Task , Kanban
from rest_framework import serializers

class KanbanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kanban
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Task
        fields = "__all__"