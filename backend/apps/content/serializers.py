from rest_framework import serializers
from .models import Post, Category, Tag, Media, Testimonial, Partner

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ("id", "name", "slug", "description")

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Tag
        fields = ("id", "name", "slug")

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.full_name", read_only=True)
    category    = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category", queryset=Category.objects.all(), write_only=True, required=False
    )
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model  = Post
        fields = ("id", "title", "slug", "excerpt", "featured_image", "author_name",
                  "category", "category_id", "tags", "status", "is_featured",
                  "view_count", "read_time", "published_at", "created_at")
        read_only_fields = ("id", "slug", "view_count", "published_at", "created_at")

class PostDetailSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ("body", "meta_title", "meta_desc", "updated_at")

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Media
        fields = ("id", "name", "file", "file_type", "file_size", "alt_text", "created_at")
        read_only_fields = ("id", "file_type", "file_size", "created_at")

    def create(self, validated_data):
        file = validated_data["file"]
        validated_data["file_type"] = file.content_type
        validated_data["file_size"] = file.size
        validated_data["uploaded_by"] = self.context["request"].user
        return super().create(validated_data)

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Testimonial
        fields = ("id", "author_name", "author_role", "avatar", "body", "rating")

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Partner
        fields = ("id", "name", "logo", "url")
