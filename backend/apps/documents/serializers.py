from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    category_name   = serializers.CharField(source="category.name", read_only=True)
    uploaded_by_name = serializers.CharField(source="uploaded_by.full_name", read_only=True)
    class Meta:
        model  = Document
        fields = ("id", "title", "description", "file", "file_size", "file_type",
                  "access_level", "category", "category_name", "tags",
                  "download_count", "uploaded_by_name", "created_at")
        read_only_fields = ("id", "file_size", "file_type", "download_count", "created_at")

    def create(self, validated_data):
        file = validated_data["file"]
        validated_data["file_size"] = file.size
        validated_data["file_type"] = file.content_type
        validated_data["uploaded_by"] = self.context["request"].user
        return super().create(validated_data)
