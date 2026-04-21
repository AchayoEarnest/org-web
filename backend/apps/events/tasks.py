import logging
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_event_confirmation(self, registration_id: str):
    try:
        from .models import EventRegistration
        reg  = EventRegistration.objects.select_related("event", "user").get(id=registration_id)
        html = render_to_string("emails/event_confirmation.html", {"reg": reg, "event": reg.event})
        send_mail(
            subject=f"Registration confirmed: {reg.event.title}",
            message="",
            html_message=html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reg.user.email],
        )
    except Exception as exc:
        raise self.retry(exc=exc)

@shared_task
def send_event_reminders():
    from .models import Event, EventRegistration
    tomorrow = timezone.now() + timedelta(days=1)
    events   = Event.objects.filter(
        is_published=True,
        start_datetime__date=tomorrow.date()
    )
    for event in events:
        regs = EventRegistration.objects.filter(event=event).select_related("user")
        for reg in regs:
            try:
                html = render_to_string("emails/event_reminder.html", {"reg": reg, "event": event})
                send_mail(
                    subject=f"Reminder: {event.title} is tomorrow",
                    message="",
                    html_message=html,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[reg.user.email],
                )
            except Exception as e:
                logger.error(f"Reminder failed for {reg.user.email}: {e}")
    logger.info(f"Sent reminders for {events.count()} events")
