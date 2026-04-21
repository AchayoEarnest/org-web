from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import ContactMessage, NewsletterSubscriber
from .serializers import ContactMessageSerializer, NewsletterSerializer
from .tasks import send_contact_notification, send_welcome_newsletter

class ContactView(generics.CreateAPIView):
    serializer_class  = ContactMessageSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        msg = serializer.save(
            ip_address=self.request.META.get("REMOTE_ADDR"),
            user_agent=self.request.META.get("HTTP_USER_AGENT", "")[:500],
        )
        send_contact_notification.delay(msg.id)

class NewsletterSubscribeView(generics.GenericAPIView):
    serializer_class  = NewsletterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sub, created = NewsletterSubscriber.objects.get_or_create(
            email=serializer.validated_data["email"],
            defaults={"name": serializer.validated_data.get("name", ""), "is_active": True},
        )
        if created:
            send_welcome_newsletter.delay(sub.email)
        return Response({"detail": "Subscribed successfully." if created else "Already subscribed."})

class NewsletterUnsubscribeView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "")
        NewsletterSubscriber.objects.filter(email=email).update(is_active=False)
        return Response({"detail": "Unsubscribed."})
