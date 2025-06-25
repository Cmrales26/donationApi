from apps.tasks.models import Task
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


def get_last_task_order(campaign):
    """
    Returns the last task order for a given campaign.
    If no tasks exist, returns 0.
    """
    last_task = Task.objects.filter(campaign=campaign).order_by("-order").first()
    return last_task.order if last_task else 0


def create_task(data: dict) -> Task:
    """
    Creates a new task with the provided data.

    :param data: Dictionary containing task data.
    :return: The created Task instance.
    """
    try:
        task = Task.objects.create(**data)
        return task
    except Exception as e:
        raise ValueError(
            f"An unexpected error occurred while creating the task: {str(e)}"
        ) from e


def get_task_by_id(task_id: int) -> Task:
    """"""
    "Retrieves a Task instance by its ID."
    ""
    return get_object_or_404(Task, pk=task_id)


def update_task_status(task: Task, new_status: str) -> Task:
    """"""
    "Updates the status of a Task instance."
    ""
    task.status = new_status
    task.save(update_fields=["status"])
    return task


def get_campaign_tasks_excluding(task: Task) -> QuerySet:
    return (
        Task.objects.filter(campaign=task.campaign)
        .exclude(id=task.id)
        .order_by("order")
    )


def save_task(task: Task, update_fields: list[str] = None) -> Task:
    task.save(update_fields=update_fields)
    return task
