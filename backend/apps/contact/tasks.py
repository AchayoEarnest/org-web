import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_contact_notification(self, message_id):
    try:
        from .models import ContactMessage
        msg = ContactMessage.objects.get(id=message_id)
        send_mail(
            subject=f"[Contact] {msg.subject}",
            message=f"From: {msg.name} <{msg.email}>\n\n{msg.message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )
        send_mail(
            subject="We received your message",
            message=f"Hi {msg.name},\n\nThank you for reaching out. We will respond shortly.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[msg.email],
        )
    except Exception as exc:
        raise self.retry(exc=exc)

@shared_task
def send_welcome_newsletter(email: str):
    send_mail(
        subject="Welcome to our newsletter!",
        message="Thank you for subscribing. You will receive our latest updates.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )
