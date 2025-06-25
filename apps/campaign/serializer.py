from apps.campaign.models import Campaign
from rest_framework import serializers
from apps.user.models import User
from apps.tasks.serializer import TaskSerializer
from services.email_service import send_email


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
                    "Users in group 1 (Admins) cannot be assigned to a campaign."
                )

            taskUser = User.objects.get(username=user)

            if not taskUser:
                raise serializers.ValidationError("User does not exist.")

            email_success = send_email(
                subject="Campaign Created",
                message=f"Hello {taskUser.first_name},\n\nYour campaign has been successfully created.",
                recipient_list=[taskUser.email],
            )

            if not email_success:
                raise serializers.ValidationError(
                    "Failed to send email notification to the user."
                )

            # user who created the campaign
            created_by = self.context.get("request").user
            validated_data["create_by"] = created_by

            campaign = Campaign.objects.create(**validated_data)
            return campaign

        except serializers.ValidationError as e:
            raise e

        except Exception as e:
            raise serializers.ValidationError(f"An unexpected error occurred: {str(e)}")
