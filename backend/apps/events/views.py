from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer
from core.permissions import IsStaffOrAdmin

class EventViewSet(viewsets.ModelViewSet):
    search_fields    = ["title", "description", "location"]
    filterset_fields = ["is_published", "is_virtual", "is_free", "category"]
    ordering_fields  = ["start_datetime", "created_at"]
    lookup_field     = "slug"

    def get_queryset(self):
        qs = Event.objects.prefetch_related("registrations")
        user = self.request.user
        if not user.is_authenticated or user.role == "member":
            return qs.filter(is_published=True, start_datetime__gte=timezone.now())
        return qs.all()

    def get_serializer_class(self):
        return EventSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"): return []
        if self.action == "register": return [IsAuthenticated()]
        return [IsStaffOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def register(self, request, slug=None):
        event = self.get_object()
        if event.spots_left is not None and event.spots_left <= 0:
            return Response({"detail": "Event is fully booked."}, status=status.HTTP_400_BAD_REQUEST)
        reg, created = EventRegistration.objects.get_or_create(event=event, user=request.user)
        if not created:
            return Response({"detail": "Already registered."}, status=status.HTTP_400_BAD_REQUEST)
        from .tasks import send_event_confirmation
        send_event_confirmation.delay(str(reg.id))
        return Response(EventRegistrationSerializer(reg).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], permission_classes=[IsAuthenticated])
    def unregister(self, request, slug=None):
        event = self.get_object()
        EventRegistration.objects.filter(event=event, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
