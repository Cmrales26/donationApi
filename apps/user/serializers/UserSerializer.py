from rest_framework import serializers
from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "is_staff",
            "is_active",
        )
        read_only_fields = ("id", "is_staff", "is_active")
