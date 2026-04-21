from django.urls import path
from .views import DashboardView, PageViewTrackView

urlpatterns = [
    path("dashboard/", DashboardView.as_view()),
    path("track/",     PageViewTrackView.as_view()),
]
