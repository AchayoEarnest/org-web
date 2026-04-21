from rest_framework import serializers
from .models import Job, JobApplication

class JobSerializer(serializers.ModelSerializer):
    application_count = serializers.IntegerField(source="applications.count", read_only=True)
    class Meta:
        model  = Job
        fields = ("id", "title", "slug", "department", "location", "type",
                  "description", "requirements", "benefits", "salary_min",
                  "salary_max", "is_active", "deadline", "application_count", "created_at")
        read_only_fields = ("id", "slug", "created_at")

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = JobApplication
        fields = ("id", "job", "name", "email", "phone", "resume", "cover_letter", "applied_at")
        read_only_fields = ("id", "applied_at")

class JobApplicationAdminSerializer(JobApplicationSerializer):
    class Meta(JobApplicationSerializer.Meta):
        fields = JobApplicationSerializer.Meta.fields + ("status", "notes", "updated_at")
