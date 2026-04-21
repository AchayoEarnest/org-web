import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("email_verified", True)
        return self.create_user(email, full_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN  = "admin",  "Admin"
        STAFF  = "staff",  "Staff"
        MEMBER = "member", "Member"

    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email          = models.EmailField(unique=True)
    full_name      = models.CharField(max_length=255)
    role           = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    avatar         = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio            = models.TextField(blank=True)
    phone          = models.CharField(max_length=30, blank=True)
    is_active      = models.BooleanField(default=True)
    is_staff       = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    newsletter_sub = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["role"]),
            models.Index(fields=["created_at"]),
        ]
