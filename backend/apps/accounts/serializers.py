from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = ("email", "full_name", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password2"):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ("id", "email", "full_name", "role", "avatar", "bio",
                  "phone", "email_verified", "newsletter_sub", "created_at")
        read_only_fields = ("id", "email", "role", "email_verified", "created_at")

class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ("id", "email", "full_name", "role", "is_active",
                  "email_verified", "created_at", "last_login")
        read_only_fields = ("id", "email", "created_at", "last_login")

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
