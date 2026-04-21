import uuid
from django.db import models
from django.utils.text import slugify

class Event(models.Model):
    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title          = models.CharField(max_length=255)
    slug           = models.SlugField(unique=True)
    description    = models.TextField()
    location       = models.CharField(max_length=255, blank=True)
    is_virtual     = models.BooleanField(default=False)
    virtual_url    = models.URLField(blank=True)
    start_datetime = models.DateTimeField()
    end_datetime   = models.DateTimeField()
    capacity       = models.PositiveIntegerField(null=True, blank=True)
    featured_image = models.ImageField(upload_to="events/", null=True, blank=True)
    is_published   = models.BooleanField(default=False)
    is_free        = models.BooleanField(default=True)
    price          = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    category       = models.ForeignKey("content.Category", on_delete=models.SET_NULL, null=True, blank=True)
    created_by     = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def spots_left(self):
        if not self.capacity: return None
        return self.capacity - self.registrations.count()

    def __str__(self): return self.title
    class Meta: db_table = "events"; ordering = ["start_datetime"]

class EventRegistration(models.Model):
    event         = models.ForeignKey(Event, related_name="registrations", on_delete=models.CASCADE)
    user          = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    attended      = models.BooleanField(default=False)
    notes         = models.TextField(blank=True)
    class Meta:
        db_table       = "event_registrations"
        unique_together = ("event", "user")
