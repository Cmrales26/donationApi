from django.contrib.auth import get_user_model
from apps.campaign.models import Campaign
from apps.tasks.models import Task

User = get_user_model()


def get_dashboard_metrics() -> dict:
    return {
        "total_users": User.objects.count(),
        "total_campaigns": Campaign.objects.count(),
        "total_tasks": Task.objects.count(),
    }
