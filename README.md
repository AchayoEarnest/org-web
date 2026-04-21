# Org Website — Full-Stack Platform

A production-ready organizational website built with **Next.js 14**, **Django 5 + DRF**, **PostgreSQL**, **Redis**, and **Celery**.

## Stack

| Layer     | Technology                              |
|-----------|----------------------------------------|
| Frontend  | Next.js 14 (App Router), Tailwind CSS, Framer Motion, TanStack Query |
| Backend   | Django 5, DRF, Simple JWT             |
| Queue     | Celery + Redis                         |
| Database  | PostgreSQL 16                          |
| Storage   | AWS S3                                 |
| Auth      | NextAuth.js + Django JWT + Google OAuth|
| Deploy    | Docker + Nginx + GitHub Actions        |

## Quick Start

```bash
# 1. Clone and configure
git clone https://github.com/your-org/org-website
cd org-website
cp .env.example .env
# Edit .env with your credentials

# 2. Start infrastructure
docker-compose up -d db redis

# 3. Start application
docker-compose up -d backend celery_worker celery_beat frontend nginx

# 4. Run migrations and create superuser
docker-compose exec backend python manage.py migrate --settings=config.settings.production
docker-compose exec backend python manage.py createsuperuser --settings=config.settings.production

# 5. Open the app
# Frontend:  http://localhost:3000
# API:       http://localhost:8000/api/v1/
# API Docs:  http://localhost:8000/api/docs/
# Admin:     http://localhost:8000/admin/
```

## Local Development (without Docker)

### Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements/development.txt
cp ../.env.example .env  # configure for local
python manage.py migrate --settings=config.settings.development
python manage.py runserver --settings=config.settings.development
# In another terminal:
celery -A config worker --loglevel=info
```

### Frontend
```bash
cd frontend
npm install
cp ../.env.example .env.local  # configure NEXTAUTH_URL etc.
npm run dev
```

## Project Structure

```
org-website/
├── backend/           Django + DRF API
│   ├── config/        Settings, URLs, Celery
│   ├── apps/
│   │   ├── accounts/  Auth, users, JWT
│   │   ├── content/   Blog, CMS, media
│   │   ├── events/    Events + registrations
│   │   ├── documents/ File resource center
│   │   ├── careers/   Jobs + applications
│   │   ├── contact/   Contact forms, newsletter
│   │   ├── notifications/ In-app notifications
│   │   └── analytics/ Page tracking, KPIs
│   └── core/          Middleware, permissions, pagination
├── frontend/          Next.js 14 App Router
│   ├── app/           Pages (public + auth + dashboard)
│   ├── components/    UI, sections, forms, dashboard
│   ├── lib/           API client, auth config, utils
│   └── types/         TypeScript interfaces
├── docker-compose.yml Full stack orchestration
├── nginx.conf         Reverse proxy config
└── .github/workflows/ CI/CD pipeline
```

## API Reference

Full interactive docs at `/api/docs/` (Swagger UI).

Key endpoints:

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/v1/auth/login/` | POST | — | Login → JWT tokens |
| `/api/v1/auth/register/` | POST | — | Create account |
| `/api/v1/content/posts/` | GET | — | List published posts |
| `/api/v1/events/` | GET | — | List upcoming events |
| `/api/v1/events/{slug}/register/` | POST | JWT | Register for event |
| `/api/v1/documents/` | GET | JWT | List accessible documents |
| `/api/v1/analytics/dashboard/` | GET | Admin | KPI metrics |

## Deployment

Push to `main` to trigger the GitHub Actions pipeline which:
1. Runs backend tests
2. Runs frontend lint + type check
3. Builds and pushes Docker images to GHCR
4. SSH deploys to your server and runs migrations

See `.github/workflows/deploy.yml` for required secrets.

## Customization

- **Branding**: Update `tailwind.config.ts` colors and `app/layout.tsx` fonts
- **Organization name**: Find/replace "OrgSite" across the codebase
- **Email templates**: Edit `backend/templates/emails/`
- **Homepage content**: Edit `components/sections/`
