from rest_framework import viewsets, status
from apps.campaign.models import Campaign
from apps.campaign.serializers.CampaignSerializer import CampaignSerializer
from utils.permission import havePermission
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.campaign.services.CampaignServices import update_campaign_status
from rest_framework import serializers


class CampaignView(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [havePermission]

    def get_queryset(self):
        user = self.request.user
        status_param = self.request.query_params.get("status", None)

        valid_statuses = [choice[0] for choice in Campaign.STATUS_CHOICES]

        if user.groups.filter(id=1).exists():
            queryset = Campaign.objects.all()
        else:
            queryset = Campaign.objects.filter(user=user)

        if status_param:
            if status_param not in valid_statuses:
                raise serializers.ValidationError(
                    f"Invalid status. Valid options are: {', '.join(valid_statuses)}"
                )
            queryset = queryset.filter(status=status_param)

        return queryset

    @action(detail=True, methods=["patch"], url_path="update-status")
    def update_status(self, request, pk=None):
        new_status = request.data.get("status")
        if not new_status:
            return Response(
                {"status": "this field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            campaign = update_campaign_status(pk, new_status, request.user)
            return Response(
                CampaignSerializer(campaign).data,
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return Response(
                {"error": str(e.detail)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
