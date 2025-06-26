from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.dashboard.services import get_dashboard_metrics


class IsAdminGroup(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(id=1).exists()


class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdminGroup]

    @action(detail=False, methods=["get"], url_path="metrics")
    def metrics(self, request):
        try:
            data = get_dashboard_metrics()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
