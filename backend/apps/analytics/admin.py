from django.contrib import admin
from .models import ActivityLog, PageView

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display  = ("user", "method", "path", "status_code", "created_at")
    list_filter   = ("method", "status_code")
    readonly_fields = ("created_at",)

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ("path", "ip_address", "created_at")
    readonly_fields = ("created_at",)
