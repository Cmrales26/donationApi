from rest_framework import serializers
from apps.tasks.models import Task
from apps.tasks.services.TaskServices import update_task_with_reordering


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = (
            "id",
            "beneficiary",
        )

    def update(self, instance, validated_data):
        try:
            return update_task_with_reordering(instance, validated_data)
        except serializers.ValidationError:
            raise
        except Exception as e:
            raise serializers.ValidationError(f"An unexpected error occurred: {str(e)}")
