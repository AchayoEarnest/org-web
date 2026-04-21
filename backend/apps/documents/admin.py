from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display  = ("title", "access_level", "file_type", "download_count", "uploaded_by", "created_at")
    list_filter   = ("access_level", "file_type")
    search_fields = ("title", "description")
    raw_id_fields = ("uploaded_by",)
