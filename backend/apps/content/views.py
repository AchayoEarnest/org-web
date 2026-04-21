from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils import timezone
from django.db import models as db_models
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Category, Tag, Media, Testimonial, Partner
from .serializers import (
    PostSerializer, PostDetailSerializer, CategorySerializer,
    TagSerializer, MediaSerializer, TestimonialSerializer, PartnerSerializer,
)
from core.permissions import IsStaffOrAdmin

class CategoryViewSet(viewsets.ModelViewSet):
    queryset           = Category.objects.all()
    serializer_class   = CategorySerializer
    lookup_field       = "slug"
    search_fields      = ["name"]
    def get_permissions(self):
        if self.action in ("list", "retrieve"): return []
        return [IsStaffOrAdmin()]

class TagViewSet(viewsets.ModelViewSet):
    queryset         = Tag.objects.all()
    serializer_class = TagSerializer
    search_fields    = ["name"]
    def get_permissions(self):
        if self.action in ("list", "retrieve"): return []
        return [IsStaffOrAdmin()]

class PostViewSet(viewsets.ModelViewSet):
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "category", "is_featured"]
    search_fields    = ["title", "excerpt"]
    ordering_fields  = ["published_at", "view_count", "created_at"]
    lookup_field     = "slug"

    def get_queryset(self):
        user = self.request.user
        qs   = Post.objects.select_related("author", "category").prefetch_related("tags")
        if not user.is_authenticated or user.role == "member":
            return qs.filter(status="published", published_at__lte=timezone.now())
        return qs.all()

    def get_serializer_class(self):
        return PostDetailSerializer if self.action == "retrieve" else PostSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"): return []
        return [IsStaffOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Post.objects.filter(pk=instance.pk).update(view_count=db_models.F("view_count") + 1)
        return Response(self.get_serializer(instance).data)

    @action(detail=True, methods=["post"], permission_classes=[IsStaffOrAdmin])
    def publish(self, request, slug=None):
        post = self.get_object()
        post.status = "published"
        post.published_at = timezone.now()
        post.save(update_fields=["status", "published_at"])
        return Response({"detail": "Post published."})

class MediaViewSet(viewsets.ModelViewSet):
    queryset           = Media.objects.all().order_by("-created_at")
    serializer_class   = MediaSerializer
    permission_classes = [IsStaffOrAdmin]
    filterset_fields   = ["file_type"]
    search_fields      = ["name"]

class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset         = Testimonial.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer

class PartnerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset         = Partner.objects.filter(is_active=True)
    serializer_class = PartnerSerializer
