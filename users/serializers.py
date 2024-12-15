from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ("username",)

    def create(self, validated_data):
        validated_data["username"] = validated_data.get("email")
        return User.objects.create_user(**validated_data)


class UserSerializerWithoutPassword(UserSerializer):
    class Meta:
        model = User
        exclude = ("password", "username")
