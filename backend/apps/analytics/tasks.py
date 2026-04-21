import logging
from celery import shared_task
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)

@shared_task
def generate_daily_report():
    from .models import PageView, ActivityLog
    yesterday = timezone.now() - timedelta(days=1)
    views  = PageView.objects.filter(created_at__date=yesterday.date()).count()
    writes = ActivityLog.objects.filter(created_at__date=yesterday.date()).count()
    logger.info(f"Daily report — Views: {views}, API writes: {writes}")
    return {"views": views, "api_writes": writes}
