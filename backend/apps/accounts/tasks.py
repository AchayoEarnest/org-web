import logging
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_verification(self, user_id: str):
    try:
        from .models import User
        user  = User.objects.get(id=user_id)
        token = default_token_generator.make_token(user)
        uid   = urlsafe_base64_encode(force_bytes(user_id))
        url   = f"{settings.FRONTEND_URL}/verify-email?token={token}&uid={uid}"
        html  = render_to_string("emails/verify_email.html", {"user": user, "url": url})
        send_mail(
            subject="Verify your email",
            message=url,
            html_message=html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        logger.info(f"Verification email sent to {user.email}")
    except Exception as exc:
        logger.error(f"Failed to send verification email: {exc}")
        raise self.retry(exc=exc)

@shared_task(bind=True, max_retries=3)
def send_password_reset_email(self, email: str):
    try:
        from .models import User
        user  = User.objects.get(email=email, is_active=True)
        token = default_token_generator.make_token(user)
        uid   = urlsafe_base64_encode(force_bytes(str(user.id)))
        url   = f"{settings.FRONTEND_URL}/reset-password?token={token}&uid={uid}"
        html  = render_to_string("emails/password_reset.html", {"user": user, "url": url})
        send_mail(
            subject="Reset your password",
            message=url,
            html_message=html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
    except Exception:
        pass  # Silent — prevents email enumeration

@shared_task
def cleanup_expired_tokens():
    from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
    from django.utils import timezone
    OutstandingToken.objects.filter(expires_at__lt=timezone.now()).delete()
    logger.info("Expired JWT tokens cleaned up")
