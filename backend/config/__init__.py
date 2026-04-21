# config/__init__.py
# ─────────────────────────────────────────────────────────────────────────────
# FIX: guard the Celery import so that `python manage.py runserver` works even
#      when celery is not installed (e.g. using requirements/base.txt only).
#      Production always installs the full requirements/production.txt so this
#      never affects deployed environments.
# ─────────────────────────────────────────────────────────────────────────────

try:
    from .celery import app as celery_app
    __all__ = ("celery_app",)
except ImportError:
    # Celery not installed — fine for minimal local development
    pass
