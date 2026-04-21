# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/",                  admin.site.urls),
    path("api/v1/auth/",            include("apps.accounts.urls")),
    path("api/v1/content/",         include("apps.content.urls")),
    path("api/v1/events/",          include("apps.events.urls")),
    path("api/v1/documents/",       include("apps.documents.urls")),
    path("api/v1/careers/",         include("apps.careers.urls")),
    path("api/v1/contact/",         include("apps.contact.urls")),
    path("api/v1/notifications/",   include("apps.notifications.urls")),
    path("api/v1/analytics/",       include("apps.analytics.urls")),
    path("api/schema/",             SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/",               SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]