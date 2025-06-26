from rest_framework import viewsets, status
from apps.tasks.models import Task
from apps.tasks.serializers.TaskSerializer import TaskSerializer
from apps.tasks.serializers.TaskUpdateSerializer import TaskUpdateSerializer
from utils.permission import havePermission, IsAdminOrOwner
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.tasks.services.TaskServices import change_task_status
from rest_framework import serializers


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        """Returns the appropriate serializer class based on the action being performed."""

        if self.action in ["update", "partial_update"]:
            return TaskUpdateSerializer

        return TaskSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [havePermission]
        else:
            permission_classes = [IsAdminOrOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        campaign_id = self.request.query_params.get("campaign", None)
        status = self.request.query_params.get("status", None)

        if user.groups.filter(id=1).exists():
            queryset = Task.objects.all()
        else:
            queryset = Task.objects.filter(beneficiary=user)

        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)

        if status:
            queryset = queryset.filter(status=status)

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
            task = change_task_status(pk, new_status, request.user)
            return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response(
                {"error": str(e.detail)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Unexpected error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
