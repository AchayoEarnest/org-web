import uuid
from django.db import models

class Notification(models.Model):
    class Type(models.TextChoices):
        INFO    = "info",    "Info"
        SUCCESS = "success", "Success"
        WARNING = "warning", "Warning"
        ERROR   = "error",   "Error"

    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user       = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="notifications")
    title      = models.CharField(max_length=255)
    body       = models.TextField()
    type       = models.CharField(max_length=20, choices=Type.choices, default=Type.INFO)
    link       = models.URLField(blank=True)
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: db_table = "notifications"; ordering = ["-created_at"]
