# config/celery.py
# ─────────────────────────────────────────────────────────────────────────────
# Celery application entry point.
#
# FIX: default DJANGO_SETTINGS_MODULE changed from production → development so
#      `celery -A config worker` works locally without setting env vars first.
#      Production deployments always set DJANGO_SETTINGS_MODULE explicitly via
#      the Dockerfile CMD / docker-compose environment block anyway.
# ─────────────────────────────────────────────────────────────────────────────

import os
from celery import Celery
from celery.schedules import crontab

# Default to development; production containers override this explicitly.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("org_website")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send-event-reminders": {
        "task":     "apps.events.tasks.send_event_reminders",
        "schedule": crontab(hour=8, minute=0),
    },
    "cleanup-expired-tokens": {
        "task":     "apps.accounts.tasks.cleanup_expired_tokens",
        "schedule": crontab(hour=2, minute=0),
    },
    "generate-daily-analytics": {
        "task":     "apps.analytics.tasks.generate_daily_report",
        "schedule": crontab(hour=0, minute=30),
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
