from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView, ProfileView,
    PasswordChangeView, PasswordResetRequestView, PasswordResetConfirmView,
    UserAdminViewSet,
)

router = DefaultRouter()
router.register("users", UserAdminViewSet, basename="users")

urlpatterns = [
    path("register/",              RegisterView.as_view()),
    path("login/",                 LoginView.as_view()),
    path("logout/",                LogoutView.as_view()),
    path("token/refresh/",         TokenRefreshView.as_view()),
    path("profile/",               ProfileView.as_view()),
    path("password/change/",       PasswordChangeView.as_view()),
    path("password/reset/",        PasswordResetRequestView.as_view()),
    path("password/reset/confirm/",PasswordResetConfirmView.as_view()),
    path("", include(router.urls)),
]
