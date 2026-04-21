from django.contrib import admin
from .models import ContactMessage, NewsletterSubscriber

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ("name", "email", "subject", "status", "created_at")
    list_filter   = ("status",)
    search_fields = ("name", "email", "subject")
    readonly_fields = ("ip_address", "user_agent", "created_at")

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display  = ("email", "name", "is_active", "subscribed_at")
    list_filter   = ("is_active",)
    search_fields = ("email", "name")
