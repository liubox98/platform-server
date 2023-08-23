from rest_framework import serializers
from modules.funcition.task.models import TaskInfo, TaskEventLog


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskInfo
        fields = "__all__"


class TaskEventLogListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.order_by('-timestamp')
        return super().to_representation(data)


class TaskEventLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskEventLog
        fields = "__all__"
        list_serializer_class = TaskEventLogListSerializer
