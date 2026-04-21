# config/settings/development.py
# ─────────────────────────────────────────────────────────────────────────────
# LOCAL DEVELOPMENT settings (python manage.py runserver)
#
# Key differences from base.py:
#   • POSTGRES_HOST defaults to "localhost"  ← fixes "could not translate host
#     name 'db'" when running outside Docker
#   • Cache falls back to in-memory locmem when REDIS_URL is not set
#   • Celery runs tasks synchronously (no broker needed for basic dev)
#   • debug_toolbar only loaded when the package is actually installed
#   • EMAIL_BACKEND prints to console (no SMTP server needed)
# ─────────────────────────────────────────────────────────────────────────────

import os
from .base import *   # noqa: F401, F403

# ── Core ──────────────────────────────────────────────────────────────────────
DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True

# ── Email ─────────────────────────────────────────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ── Database ─────────────────────────────────────────────────────────────────
# Override HOST so that running locally (without Docker) resolves correctly.
# "db" is the Docker Compose service name and only valid inside a container.
# Outside Docker (plain `python manage.py runserver`) the host must be localhost.
#
# Priority:  shell env POSTGRES_HOST > .env POSTGRES_HOST > "localhost"
DATABASES["default"]["HOST"] = os.environ.get("POSTGRES_HOST", "localhost")   # noqa: F405

# ── Cache ─────────────────────────────────────────────────────────────────────
# Use Redis when REDIS_URL is set; fall back to in-memory so the server starts
# even if Redis is not running locally.
_redis_url = os.environ.get("REDIS_URL", "")
if _redis_url:
    CACHES = {
        "default": {
            "BACKEND":  "django_redis.cache.RedisCache",
            "LOCATION": _redis_url,
            "OPTIONS":  {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
            "TIMEOUT":  300,
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }

# ── Celery ────────────────────────────────────────────────────────────────────
# When there's no Redis broker, run tasks synchronously in the same process.
# This means Celery task calls work without a running worker.
if not _redis_url:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True

# ── Django Debug Toolbar (optional) ──────────────────────────────────────────
# Only add debug_toolbar if it is actually installed; prevents ImportError
# when using the minimal requirements/base.txt install.
try:
    import debug_toolbar  # noqa: F401
    INSTALLED_APPS += ["debug_toolbar"]                              # noqa: F405
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE  # noqa: F405
    INTERNAL_IPS = ["127.0.0.1"]
except ImportError:
    pass
