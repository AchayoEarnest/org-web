from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from .models import ActivityLog, PageView
from apps.accounts.models import User
from apps.content.models import Post
from apps.events.models import Event
from core.permissions import IsAdmin

class DashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        now       = timezone.now()
        month_ago = now - timedelta(days=30)
        week_ago  = now - timedelta(days=7)

        users_qs    = User.objects.all()
        new_signups = users_qs.filter(created_at__gte=week_ago).count()

        views_by_day = (
            PageView.objects.filter(created_at__gte=month_ago)
            .extra(select={"day": "date(created_at)"})
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        return Response({
            "users":       users_qs.count(),
            "signups":     new_signups,
            "page_views":  PageView.objects.filter(created_at__gte=month_ago).count(),
            "posts":       Post.objects.filter(status="published").count(),
            "events":      Event.objects.filter(is_published=True, end_datetime__gte=now).count(),
            "views_chart": list(views_by_day),
            "users_by_role": list(
                users_qs.values("role").annotate(count=Count("id"))
            ),
        })

class PageViewTrackView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        PageView.objects.create(
            path=request.data.get("path", "")[:500],
            referer=request.data.get("referer", "")[:500],
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
            ip_address=request.META.get("REMOTE_ADDR"),
        )
        return Response({"ok": True})
