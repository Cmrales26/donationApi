from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from apps.tasks.models import Task
from apps.tasks.serializer import TaskSerializer, TaskUpdateSerializer
from utils.permission import havePermission, IsAdminOrOwner
from rest_framework.response import Response
from rest_framework.decorators import action


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

        if user.groups.filter(id=1).exists():
            return Task.objects.all()
        else:
            return Task.objects.filter(beneficiary=user)

    @action(detail=True, methods=["patch"], url_path="update-status")
    def update_status(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)

        is_admin = request.user.groups.filter(id=1).exists()
        is_owner = request.user == task.beneficiary

        ""
        " Verificar si el usuario tiene permiso para modificar la tarea"
        ""

        if not (is_admin or is_owner):
            return Response(
                {"detail": "No access to modify this task."},
                status=status.HTTP_403_FORBIDDEN,
            )

        new_status = request.data.get("status")
        if not new_status:
            return Response(
                {"status": "this field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_statuses = [choice[0] for choice in Task.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {
                    "status": f"Estado inválido. Opciones válidas: {', '.join(valid_statuses)}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            task.status == Task.STATUS_CHOICES[2][0]
            and new_status != Task.STATUS_CHOICES[2][0]
        ):
            return Response(
                {"status": "Cannot change status from completed to another state."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        task.status = new_status
        task.save()

        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_200_OK,
        )
