from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models as db_models
from .models import Document
from .serializers import DocumentSerializer
from core.permissions import IsStaffOrAdmin, DocumentAccessPermission

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    filterset_fields = ["access_level", "category"]
    search_fields    = ["title", "description"]

    def get_queryset(self):
        user = self.request.user
        qs   = Document.objects.select_related("category", "uploaded_by").prefetch_related("tags")
        if not user.is_authenticated:
            return qs.filter(access_level="public")
        if user.role == "member":
            return qs.filter(access_level__in=["public", "members"])
        if user.role == "staff":
            return qs.filter(access_level__in=["public", "members", "staff"])
        return qs.all()

    def get_permissions(self):
        if self.action in ("list", "retrieve", "download"): return [DocumentAccessPermission()]
        return [IsStaffOrAdmin()]

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        doc = self.get_object()
        self.check_object_permissions(request, doc)
        Document.objects.filter(pk=doc.pk).update(download_count=db_models.F("download_count") + 1)
        return Response({"url": request.build_absolute_uri(doc.file.url)})
