from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerialier(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def get_fields(self):
        fields = super().get_fields()

        exclude_fields = self.context.get("exclude_fields", [])
        for field in exclude_fields:
            fields.pop(field)

        return fields

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
