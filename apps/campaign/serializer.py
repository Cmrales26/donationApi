from apps.campaign.models import Campaign
from rest_framework import serializers
from apps.user.serializer import UserSerializer
from apps.tasks.serializer import TaskSerializer


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

    def get_queryset(self):
        """
        Override to filter campaigns based on the user's group.
        Only users in group 1 (Admons) can see all campaigns.
        Other users can only see their own campaigns.
        """

    def create(self, validated_data):
        try:
            user = validated_data.get("user")
            if user and user.groups.filter(id=1).exists():
                raise serializers.ValidationError(
                    "Users in group 1 (Admons) cannot be assigned to a campaign."
                )

            campaign = Campaign.objects.create(**validated_data)
            return campaign

        except serializers.ValidationError as e:
            raise e

        except Exception as e:
            raise serializers.ValidationError(f"An unexpected error occurred: {str(e)}")
