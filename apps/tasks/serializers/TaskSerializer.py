from rest_framework import serializers
from apps.tasks.models import Task
from apps.tasks.services.TaskServices import (
    create_task_service as create_task_for_campaign,
)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("id", "beneficiary", "order")

    def create(self, validated_data):
        try:
            return create_task_for_campaign(validated_data)
        except serializers.ValidationError:
            raise
        except Exception as e:
            raise serializers.ValidationError(f"An unexpected error occurred: {str(e)}")
