from apps.user.models import User
from rest_framework import viewsets, permissions

from apps.user.serializers.UserSerializer import UserSerializer
from apps.user.serializers.UserCreateSerializer import UserCreateSerializer
from apps.user.serializers.TokenObtainPairSerializer import TokenObtainPairSerializer
from apps.user.services.UserService import get_users_filtered

from rest_framework_simplejwt.views import TokenObtainPairView


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == "list":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        group_id = self.request.query_params.get("user_grup")
        return get_users_filtered(group_id)


class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
