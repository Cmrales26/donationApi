from rest_framework import serializers
from apps.user.serializer import UserSerializer
from apps.tasks.models import Task
from apps.campaign.models import Campaign


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("id", "beneficiary", "order")

    def create(self, validated_data):
        campaign = validated_data.get("campaign")

        if not campaign:
            raise serializers.ValidationError("Campaign is required to create a task.")

        if not campaign.user:
            raise serializers.ValidationError("Campaign must have an associated user.")

        validated_data["beneficiary"] = campaign.user

        ""
        "Set the order of the task based on the last task in the campaign."
        ""

        last_task = Task.objects.filter(campaign=campaign).order_by("-order").first()
        next_order = last_task.order + 1 if last_task else 1
        validated_data["order"] = next_order

        if (
            campaign.status == Campaign.STATUS_CHOICES[2][0]
            or campaign.status == Campaign.STATUS_CHOICES[1][0]
        ):
            raise serializers.ValidationError(
                "Cannot create a task for a campaign that is closed or canceled."
            )

        try:
            task = Task.objects.create(**validated_data)
            return task
        except Exception as e:
            raise serializers.ValidationError(f"An unexpected error occurred: {str(e)}")


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = (
            "id",
            "beneficiary",
        )

    def update(self, instance, validated_data):
        """
        Updates a Task instance, handling reordering within its campaign if the 'order' field changes.

        If the 'order' value is updated, this method:
            - Retrieves all tasks in the same campaign, excluding the current instance.
            - Inserts the current instance into the new position in the ordered list.
            - Reassigns the 'order' field for all affected tasks to maintain a contiguous sequence.
            - Updates the current instance's 'order' field.

        After handling reordering, updates any other fields provided in validated_data.

        Args:
            instance (Task): The Task instance to update.
            validated_data (dict): Dictionary of fields to update on the instance.

        Returns:
            Task: The updated Task instance.
        """

        new_order = validated_data.get("order", instance.order)
        campaign = instance.campaign

        if new_order != instance.order:
            tasks = (
                Task.objects.filter(campaign=campaign)
                .exclude(id=instance.id)
                .order_by("order")
            )
            tasks_list = list(tasks)
            total_tasks = len(tasks_list) + 1
            tasks_list.insert(new_order - 1, instance)

            if new_order < 1 or new_order > total_tasks:
                raise serializers.ValidationError(
                    f"Order must be between 1 and {total_tasks}."
                )

            for idx, task in enumerate(tasks_list, start=1):
                if task.id == instance.id:
                    continue
                if task.order != idx:
                    task.order = idx
                    task.save(update_fields=["order"])
            validated_data["order"] = new_order

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
