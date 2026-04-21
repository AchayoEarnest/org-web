from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import User
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    UserProfileSerializer, UserAdminSerializer, PasswordChangeSerializer,
)
from .tasks import send_email_verification, send_password_reset_email
from core.permissions import IsAdmin

class RegisterView(generics.CreateAPIView):
    serializer_class  = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_email_verification.delay(str(user.id))
        refresh = RefreshToken.for_user(user)
        return Response({
            "user":   UserProfileSerializer(user).data,
            "tokens": {"access": str(refresh.access_token), "refresh": str(refresh)},
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class  = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if not user or not user.is_active:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            "user":   UserProfileSerializer(user).data,
            "tokens": {"access": str(refresh.access_token), "refresh": str(refresh)},
        })

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data["refresh"])
            token.blacklist()
        except Exception:
            pass
        return Response({"detail": "Logged out."}, status=status.HTTP_205_RESET_CONTENT)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class  = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class PasswordChangeView(generics.GenericAPIView):
    serializer_class  = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"detail": "Wrong current password."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        return Response({"detail": "Password updated."})

class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "")
        send_password_reset_email.delay(email)
        return Response({"detail": "If this email exists, a reset link was sent."})

class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid   = request.data.get("uid")
        token = request.data.get("token")
        pwd   = request.data.get("new_password")
        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)
            if not default_token_generator.check_token(user, token):
                return Response({"detail": "Invalid or expired token."}, status=400)
            user.set_password(pwd)
            user.save(update_fields=["password"])
            return Response({"detail": "Password reset successful."})
        except Exception:
            return Response({"detail": "Invalid reset link."}, status=400)

class UserAdminViewSet(viewsets.ModelViewSet):
    queryset           = User.objects.all().order_by("-created_at")
    serializer_class   = UserAdminSerializer
    permission_classes = [IsAdmin]
    search_fields      = ["email", "full_name"]
    filterset_fields   = ["role", "is_active"]

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save(update_fields=["is_active"])
        return Response({"detail": "User deactivated."})
