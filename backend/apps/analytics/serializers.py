from rest_framework import serializers
from .models import ActivityLog, PageView

class ActivityLogSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    class Meta:
        model  = ActivityLog
        fields = ("id", "user_email", "method", "path", "status_code", "created_at")

class PageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PageView
        fields = ("id", "path", "created_at")
