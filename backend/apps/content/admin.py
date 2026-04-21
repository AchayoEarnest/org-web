from django.contrib import admin
from .models import Post, Category, Tag, Media, Testimonial, Partner

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ("title", "author", "status", "is_featured", "view_count", "published_at")
    list_filter   = ("status", "is_featured", "category")
    search_fields = ("title", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    date_hierarchy = "published_at"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Tag)
admin.site.register(Media)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author_name", "author_role", "rating", "is_active", "order")
    list_editable = ("is_active", "order")

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "is_active", "order")
    list_editable = ("is_active", "order")
