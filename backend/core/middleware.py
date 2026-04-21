import time
import logging
from django.core.cache import cache
from django.http import JsonResponse

logger = logging.getLogger(__name__)

RATE_LIMITS = {
    "/api/v1/auth/login/":    (5,   60),
    "/api/v1/auth/register/": (10,  60),
    "/api/v1/contact/":       (3,   300),
    "default":                (120, 60),
}

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/"):
            limit, window = RATE_LIMITS.get(request.path, RATE_LIMITS["default"])
            ip = self._get_ip(request)
            key = f"rl:{ip}:{request.path}"
            count = cache.get(key, 0)
            if count >= limit:
                return JsonResponse(
                    {"detail": "Rate limit exceeded. Try again later."},
                    status=429,
                    headers={"Retry-After": str(window)},
                )
            pipeline = cache.client.get_client().pipeline()
            pipeline.incr(key)
            pipeline.expire(key, window)
            pipeline.execute()
        return self.get_response(request)

    def _get_ip(self, request):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        return forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR", "0.0.0.0")


class ActivityLoggingMiddleware:
    WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (
            request.user.is_authenticated
            and request.method in self.WRITE_METHODS
            and request.path.startswith("/api/")
        ):
            try:
                from apps.analytics.models import ActivityLog
                ActivityLog.objects.create(
                    user=request.user,
                    method=request.method,
                    path=request.path,
                    status_code=response.status_code,
                    ip_address=self._get_ip(request),
                )
            except Exception as e:
                logger.warning(f"Activity log failed: {e}")
        return response

    def _get_ip(self, request):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        return forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR", "0.0.0.0")
