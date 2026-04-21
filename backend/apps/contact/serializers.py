from rest_framework import serializers
from .models import ContactMessage, NewsletterSubscriber

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ContactMessage
        fields = ("id", "name", "email", "subject", "message", "created_at")
        read_only_fields = ("id", "created_at")

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model  = NewsletterSubscriber
        fields = ("email", "name")
