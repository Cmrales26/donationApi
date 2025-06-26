from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email

        if user.groups.exists():
            token["role"] = user.groups.first().name
        else:
            token["role"] = None

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["username"] = self.user.username
        data["email"] = self.user.email

        if self.user.groups.exists():
            data["role"] = self.user.groups.first().name
        else:
            data["role"] = None
        return data
