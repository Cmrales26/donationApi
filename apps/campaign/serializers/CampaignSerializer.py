from apps.campaign.models import Campaign
from rest_framework import serializers
from apps.user.models import User
from apps.tasks.serializer import TaskSerializer
from apps.campaign.services.CampaignServices import create_campaign


class CampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    user_data = serializers.SerializerMethodField()

    def get_user_data(self, obj):
        user = obj.user
        if user:
            return {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        return None

    tasks = TaskSerializer(many=True, read_only=True)

    def create(self, validated_data):
        try:
            current_user = self.context.get("request").user
            return create_campaign(validated_data, current_user)
        except serializers.ValidationError:
            raise
        except Exception as e:
            raise serializers.ValidationError(f"An unexpected error occurred: {str(e)}")
