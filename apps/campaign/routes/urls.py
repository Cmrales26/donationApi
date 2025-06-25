from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.campaign.controllers.views import CampaignView


router = DefaultRouter()
router.register(r"campaign", CampaignView, basename="campaign")

urlpatterns = [
    path("", include(router.urls)),
]
