from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from apps.campaign.models import Campaign
from apps.campaign.serializer import CampaignSerializer
from utils.permission import havePermission
from rest_framework.response import Response
from rest_framework.decorators import action


class CampaignView(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [havePermission]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(id=1).exists():
            return Campaign.objects.all()
        else:
            return Campaign.objects.filter(user=user)

    @action(detail=True, methods=["patch"], url_path="update-status")
    def update_status(self, request, pk=None):
        campaign = get_object_or_404(Campaign, pk=pk)

        is_admin = request.user.groups.filter(id=1).exists()

        ""
        " Verificar si el usuario tiene permiso para modificar la campaña"
        if not (is_admin):
            return Response(
                {"detail": "No access to modify this campaign."},
                status=status.HTTP_403_FORBIDDEN,
            )

        ""
        " Validar que se envíe un nuevo estado"
        ""
        new_status = request.data.get("status")
        if not new_status:
            return Response(
                {"status": "this field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ""
        " Validar que el nuevo estado sea uno de los estados válidos"
        ""
        valid_statuses = [choice[0] for choice in Campaign.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {
                    "status": f"Estado inválido. Opciones válidas: {', '.join(valid_statuses)}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        ""
        " Actualizar el estado de la campaña"
        ""
        campaign.status = new_status
        campaign.save()

        return Response(
            {"status": "status change successfully", "new_status": new_status},
            status=status.HTTP_200_OK,
        )
