from apps.user.models import User
from services.email_service import send_email
from apps.campaign.repositories.CampignRespository import (
    save_campaign,
    get_campaign_by_id,
    update_campaign_status_respository,
)
from rest_framework import serializers
from apps.campaign.models import Campaign


def create_campaign(validated_data: dict, current_user: User) -> Campaign:
    user = validated_data.get("user")

    if user and user.groups.filter(id=1).exists():
        raise serializers.ValidationError(
            "Users in group 1 (Admins) cannot be assigned to a campaign."
        )

    try:
        task_user = User.objects.get(username=user.username)
    except User.DoesNotExist:
        raise serializers.ValidationError("User does not exist.")

    # Enviar correo
    email_success = send_email(
        subject="Campaign Created",
        message=f"Hello {task_user.first_name},\n\nYour campaign has been successfully created.",
        recipient_list=[task_user.email],
    )

    if not email_success:
        raise serializers.ValidationError(
            "Failed to send email notification to the user."
        )

    validated_data["create_by"] = current_user
    return save_campaign(validated_data)


def update_campaign_status(pk: int, new_status: str, user) -> Campaign:
    campaign = get_campaign_by_id(pk)

    is_admin = user.groups.filter(id=1).exists()

    if not is_admin:
        raise serializers.ValidationError("No access to modify this campaign.")

    valid_statuses = [choice[0] for choice in Campaign.STATUS_CHOICES]

    if new_status not in valid_statuses:
        raise serializers.ValidationError(
            f"Invalid status. Valid options: {', '.join(valid_statuses)}"
        )

    return update_campaign_status_respository(
        campaign,
        new_status,
    )
