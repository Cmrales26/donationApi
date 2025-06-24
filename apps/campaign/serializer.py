from apps.campaign.models import Campaign
from rest_framework import serializers


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign._meta.get_field("user").related_model
        fields = ("first_name", "last_name", "email")


class CampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    user_data = UserInfoSerializer(source="user", read_only=True)

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

            print("Creating a new campaign with data:", validated_data)
            campaign = Campaign.objects.create(**validated_data)
            return campaign

        except serializers.ValidationError as e:
            raise e  # Re-lanzamos el error para que lo capture DRF y lo devuelva como 400

        except Exception as e:
            # Captura cualquier otro error inesperado
            raise serializers.ValidationError(f"An unexpected error occurred: {str(e)}")
