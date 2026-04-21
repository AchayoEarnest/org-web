import uuid
from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    slug        = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self): return self.name
    class Meta: db_table = "categories"; verbose_name_plural = "categories"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self): return self.name
    class Meta: db_table = "tags"

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT     = "draft",     "Draft"
        REVIEW    = "review",    "In Review"
        PUBLISHED = "published", "Published"
        ARCHIVED  = "archived",  "Archived"

    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title          = models.CharField(max_length=300)
    slug           = models.SlugField(unique=True, max_length=300)
    excerpt        = models.TextField(max_length=500)
    body           = models.JSONField(default=dict)
    featured_image = models.ImageField(upload_to="posts/%Y/%m/", null=True, blank=True)
    author         = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, related_name="posts")
    category       = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="posts")
    tags           = models.ManyToManyField(Tag, blank=True)
    status         = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_featured    = models.BooleanField(default=False)
    meta_title     = models.CharField(max_length=70, blank=True)
    meta_desc      = models.CharField(max_length=160, blank=True)
    view_count     = models.PositiveIntegerField(default=0)
    read_time      = models.PositiveSmallIntegerField(default=1)
    published_at   = models.DateTimeField(null=True, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self): return self.title
    class Meta:
        db_table = "posts"
        ordering = ["-published_at"]
        indexes  = [
            models.Index(fields=["status", "published_at"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["author"]),
        ]

class Media(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name        = models.CharField(max_length=255)
    file        = models.FileField(upload_to="media/%Y/%m/")
    file_type   = models.CharField(max_length=50)
    file_size   = models.PositiveIntegerField()
    alt_text    = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
    class Meta: db_table = "media"; verbose_name_plural = "media"

class Testimonial(models.Model):
    author_name = models.CharField(max_length=100)
    author_role = models.CharField(max_length=100)
    avatar      = models.ImageField(upload_to="testimonials/", null=True, blank=True)
    body        = models.TextField()
    rating      = models.PositiveSmallIntegerField(default=5)
    is_active   = models.BooleanField(default=True)
    order       = models.PositiveSmallIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)
    class Meta: db_table = "testimonials"; ordering = ["order"]

class Partner(models.Model):
    name       = models.CharField(max_length=100)
    logo       = models.ImageField(upload_to="partners/")
    url        = models.URLField(blank=True)
    is_active  = models.BooleanField(default=True)
    order      = models.PositiveSmallIntegerField(default=0)
    class Meta: db_table = "partners"; ordering = ["order"]
