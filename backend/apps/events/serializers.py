from rest_framework import serializers
from .models import Event, EventRegistration

class EventSerializer(serializers.ModelSerializer):
    spots_left       = serializers.ReadOnlyField()
    registration_count = serializers.IntegerField(source="registrations.count", read_only=True)
    class Meta:
        model  = Event
        fields = ("id", "title", "slug", "description", "location", "is_virtual",
                  "virtual_url", "start_datetime", "end_datetime", "capacity",
                  "featured_image", "is_published", "is_free", "price",
                  "spots_left", "registration_count", "created_at")
        read_only_fields = ("id", "slug", "created_at")

class EventRegistrationSerializer(serializers.ModelSerializer):
    user_name  = serializers.CharField(source="user.full_name", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    class Meta:
        model  = EventRegistration
        fields = ("id", "event", "user_name", "user_email", "registered_at", "attended")
        read_only_fields = ("id", "registered_at")
