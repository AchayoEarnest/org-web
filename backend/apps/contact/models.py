from django.db import models

class ContactMessage(models.Model):
    class Status(models.TextChoices):
        NEW      = "new",      "New"
        READ     = "read",     "Read"
        REPLIED  = "replied",  "Replied"
        ARCHIVED = "archived", "Archived"

    name       = models.CharField(max_length=255)
    email      = models.EmailField()
    subject    = models.CharField(max_length=255)
    message    = models.TextField()
    status     = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"{self.name}: {self.subject}"
    class Meta: db_table = "contact_messages"; ordering = ["-created_at"]

class NewsletterSubscriber(models.Model):
    email        = models.EmailField(unique=True)
    name         = models.CharField(max_length=255, blank=True)
    is_active    = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    class Meta: db_table = "newsletter_subscribers"
