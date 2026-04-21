from django.contrib import admin
from .models import Job, JobApplication

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display  = ("title", "department", "type", "location", "is_active", "deadline")
    list_filter   = ("type", "is_active", "department")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display  = ("name", "email", "job", "status", "applied_at")
    list_filter   = ("status",)
    search_fields = ("name", "email")
    raw_id_fields = ("job", "applicant")
    readonly_fields = ("applied_at",)
