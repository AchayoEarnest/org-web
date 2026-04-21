from django.contrib import admin
from .models import Event, EventRegistration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display  = ("title", "start_datetime", "end_datetime", "is_published", "is_virtual", "capacity")
    list_filter   = ("is_published", "is_virtual", "is_free")
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "start_datetime"

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "registered_at", "attended")
    list_filter  = ("attended",)
    raw_id_fields = ("event", "user")
