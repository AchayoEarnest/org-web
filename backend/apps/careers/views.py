from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer, JobApplicationAdminSerializer
from core.permissions import IsStaffOrAdmin

class JobViewSet(viewsets.ModelViewSet):
    filterset_fields = ["type", "department", "is_active"]
    search_fields    = ["title", "description", "location"]
    lookup_field     = "slug"

    def get_queryset(self):
        user = self.request.user
        qs   = Job.objects.all()
        if not user.is_authenticated or user.role == "member":
            return qs.filter(is_active=True)
        return qs

    def get_serializer_class(self): return JobSerializer
    def get_permissions(self):
        if self.action in ("list", "retrieve"): return []
        return [IsStaffOrAdmin()]
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class JobApplicationViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        if user.role in ("admin", "staff"):
            return JobApplication.objects.select_related("job").all()
        return JobApplication.objects.filter(applicant=user)

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated and user.role in ("admin", "staff"):
            return JobApplicationAdminSerializer
        return JobApplicationSerializer

    def perform_create(self, serializer):
        user = self.request.user
        applicant = user if user.is_authenticated else None
        serializer.save(applicant=applicant)
