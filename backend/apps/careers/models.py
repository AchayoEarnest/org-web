import uuid
from django.db import models
from django.utils.text import slugify

class Job(models.Model):
    class Type(models.TextChoices):
        FULL_TIME  = "full_time",  "Full Time"
        PART_TIME  = "part_time",  "Part Time"
        CONTRACT   = "contract",   "Contract"
        INTERNSHIP = "internship", "Internship"
        VOLUNTEER  = "volunteer",  "Volunteer"

    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title        = models.CharField(max_length=255)
    slug         = models.SlugField(unique=True)
    department   = models.CharField(max_length=100)
    location     = models.CharField(max_length=100)
    type         = models.CharField(max_length=20, choices=Type.choices)
    description  = models.TextField()
    requirements = models.TextField()
    benefits     = models.TextField(blank=True)
    salary_min   = models.PositiveIntegerField(null=True, blank=True)
    salary_max   = models.PositiveIntegerField(null=True, blank=True)
    is_active    = models.BooleanField(default=True)
    deadline     = models.DateField(null=True, blank=True)
    created_by   = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self): return self.title
    class Meta: db_table = "jobs"; ordering = ["-created_at"]

class JobApplication(models.Model):
    class Status(models.TextChoices):
        PENDING   = "pending",   "Pending"
        REVIEWING = "reviewing", "Reviewing"
        INTERVIEW = "interview", "Interview"
        OFFERED   = "offered",   "Offered"
        REJECTED  = "rejected",  "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"

    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job          = models.ForeignKey(Job, related_name="applications", on_delete=models.CASCADE)
    applicant    = models.ForeignKey("accounts.User", on_delete=models.CASCADE, null=True, blank=True)
    name         = models.CharField(max_length=255)
    email        = models.EmailField()
    phone        = models.CharField(max_length=30, blank=True)
    resume       = models.FileField(upload_to="resumes/%Y/")
    cover_letter = models.TextField(blank=True)
    status       = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes        = models.TextField(blank=True)
    applied_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self): return f"{self.name} → {self.job.title}"
    class Meta: db_table = "job_applications"; ordering = ["-applied_at"]
