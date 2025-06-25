from apps.tasks.repositories.TaskRespository import (
    get_last_task_order,
    create_task,
    get_campaign_tasks_excluding,
    save_task,
    get_task_by_id,
    update_task_status,
)
from services.email_service import send_email
from apps.tasks.models import Task
from apps.campaign.models import Campaign
from rest_framework import serializers


def create_task_service(data: dict) -> Task:
    """
    Service function to create a new task with the provided data.

    :param data: Dictionary containing task data.
    :return: The created Task instance.
    """
    campaign = data.get("campaign")

    if not campaign:
        raise serializers.ValidationError("Campaign is required to create a task.")

    if not campaign.user:
        raise serializers.ValidationError("Campaign must have an associated user.")

    if campaign.status in [
        Campaign.STATUS_CHOICES[2][0],
        Campaign.STATUS_CHOICES[1][0],
    ]:
        raise serializers.ValidationError(
            "Cannot create a task for a campaign that is closed or canceled."
        )

    data["beneficiary"] = campaign.user

    ""
    "Set the order of the task based on the last task in the campaign."
    ""

    last_task = get_last_task_order(campaign)
    data["order"] = last_task + 1 if last_task else 1

    try:
        task = create_task(data)
        return task
    except ValueError as e:
        raise serializers.ValidationError(f"An unexpected error occurred: {str(e)}")
    except Exception as e:
        raise serializers.ValidationError(f"An unexpected error occurred: {str(e)}")


def update_task_with_reordering(instance: Task, validated_data: dict) -> Task:
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

    if new_order != instance.order:
        tasks = list(get_campaign_tasks_excluding(instance))
        total_tasks = len(tasks) + 1

        if new_order < 1 or new_order > total_tasks:
            raise serializers.ValidationError(
                f"Order must be between 1 and {total_tasks}."
            )

        tasks.insert(new_order - 1, instance)

        for idx, task in enumerate(tasks, start=1):
            if task.id == instance.id:
                continue
            if task.order != idx:
                task.order = idx
                save_task(task, update_fields=["order"])

        validated_data["order"] = new_order

    for attr, value in validated_data.items():
        setattr(instance, attr, value)

    instance.save()
    return instance


def change_task_status(task_id: int, new_status: str, current_user) -> Task:
    task = get_task_by_id(task_id)

    is_admin = current_user.groups.filter(id=1).exists()
    is_owner = current_user == task.beneficiary

    if not (is_admin or is_owner):
        raise serializers.ValidationError("No access to modify this task.")

    valid_statuses = [choice[0] for choice in Task.STATUS_CHOICES]
    if new_status not in valid_statuses:
        raise serializers.ValidationError(
            f"Invalid status. Valid options: {', '.join(valid_statuses)}"
        )

    if (
        task.status == Task.STATUS_CHOICES[2][0]
        and new_status != Task.STATUS_CHOICES[2][0]
    ):
        raise serializers.ValidationError(
            "Cannot change status from completed to another state."
        )

    campaign = Campaign.objects.get(id=task.campaign_id)
    admin_email = campaign.create_by.email

    email_success = send_email(
        subject="Task Status Update",
        message=f"Hello Admin,\n\nThe status of the task '{task.title}' has been updated to '{new_status}'.",
        recipient_list=[admin_email],
    )

    if not email_success:
        raise serializers.ValidationError("Failed to send email notification.")

    return update_task_status(task, new_status)
