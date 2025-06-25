from apps.campaign.models import Campaign
from django.shortcuts import get_object_or_404


def save_campaign(data: dict) -> Campaign:
    return Campaign.objects.create(**data)


def get_campaign_by_id(pk: int) -> Campaign:
    return get_object_or_404(Campaign, pk=pk)


def update_campaign_status_respository(campaign: Campaign, new_status: str) -> Campaign:
    campaign.status = new_status
    campaign.save()
    return campaign
