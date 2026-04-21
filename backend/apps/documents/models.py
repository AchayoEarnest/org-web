import uuid
from django.db import models

class Document(models.Model):
    class Access(models.TextChoices):
        PUBLIC  = "public",  "Public"
        MEMBERS = "members", "Members only"
        STAFF   = "staff",   "Staff only"
        ADMIN   = "admin",   "Admin only"

    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title          = models.CharField(max_length=255)
    description    = models.TextField(blank=True)
    file           = models.FileField(upload_to="documents/%Y/%m/")
    file_size      = models.PositiveIntegerField()
    file_type      = models.CharField(max_length=100)
    access_level   = models.CharField(max_length=20, choices=Access.choices, default=Access.PUBLIC)
    category       = models.ForeignKey("content.Category", null=True, blank=True, on_delete=models.SET_NULL)
    tags           = models.ManyToManyField("content.Tag", blank=True)
    download_count = models.PositiveIntegerField(default=0)
    uploaded_by    = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self): return self.title
    class Meta: db_table = "documents"; ordering = ["-created_at"]
