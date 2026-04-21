from django.db import models

class ActivityLog(models.Model):
    user        = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True)
    method      = models.CharField(max_length=10)
    path        = models.CharField(max_length=500)
    status_code = models.PositiveSmallIntegerField()
    ip_address  = models.GenericIPAddressField(null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    class Meta: db_table = "activity_logs"; ordering = ["-created_at"]

class PageView(models.Model):
    path       = models.CharField(max_length=500)
    referer    = models.CharField(max_length=500, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    ip_address = models.GenericIPAddressField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: db_table = "page_views"; ordering = ["-created_at"]
