from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField()

    class Meta:
        model = User
        fields = ("name", "phone_number", "email", "password")
        extra_kwargs = {"email": {"required": False}}

    def validate_phone_number(self, value):
        if not all(char.isdigit() or char in "+-" for char in value):
            raise serializers.ValidationError("Phone number must contain only digits, '+' or '-'.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "phone_number", "email", "status")
        read_only_fields = ("id", "phone_number", "status")


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
