from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display   = ("email", "full_name", "role", "is_active", "email_verified", "created_at")
    list_filter    = ("role", "is_active", "email_verified")
    search_fields  = ("email", "full_name")
    ordering       = ("-created_at",)
    fieldsets = (
        (None,           {"fields": ("email", "password")}),
        ("Personal",     {"fields": ("full_name", "avatar", "bio", "phone")}),
        ("Permissions",  {"fields": ("role", "is_active", "is_staff", "is_superuser", "email_verified")}),
        ("Timestamps",   {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "full_name", "password1", "password2", "role")}),
    )
    readonly_fields = ("created_at", "updated_at")
