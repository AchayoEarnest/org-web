#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# local_setup.sh  —  Bootstrap the org-website backend for local development
#
# Run from the PROJECT ROOT:
#   bash local_setup.sh
#
# What it does:
#   1. Checks PostgreSQL is running and creates the database
#   2. Creates/activates a Python virtualenv inside backend/
#   3. Installs requirements/base.txt  (no Celery/Redis required)
#   4. Copies .env.local → backend/.env if no .env exists
#   5. Runs migrations
#   6. Prints the runserver command
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

BACKEND_DIR="$(cd "$(dirname "$0")/backend" && pwd)"
FRONTEND_DIR="$(cd "$(dirname "$0")/frontend" && pwd)"

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  org-website  —  Local Dev Setup                ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# ── 1. PostgreSQL check ───────────────────────────────────────────────────────
echo "── PostgreSQL ───────────────────────────────────────"
if ! command -v pg_isready &>/dev/null || ! pg_isready -q 2>/dev/null; then
    echo "⚠  PostgreSQL not running. Starting via Homebrew..."
    brew services start postgresql@16 2>/dev/null \
    || brew services start postgresql@15 2>/dev/null \
    || brew services start postgresql   2>/dev/null \
    || true
    sleep 2
fi

if ! pg_isready -q 2>/dev/null; then
    echo ""
    echo "  ❌ PostgreSQL still not running. Start it manually:"
    echo "     brew services start postgresql@16"
    echo "  Or use Docker:"
    echo "     docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:16-alpine"
    echo ""
    exit 1
fi
echo "✓  PostgreSQL is running"

DB_NAME="${POSTGRES_DB:-org_website}"
DB_USER="${POSTGRES_USER:-postgres}"
if psql -U "$DB_USER" -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "✓  Database '$DB_NAME' already exists"
else
    echo "   Creating database '$DB_NAME'..."
    createdb -U "$DB_USER" "$DB_NAME" && echo "✓  Database '$DB_NAME' created"
fi

# ── 2. Python virtualenv ──────────────────────────────────────────────────────
echo ""
echo "── Python virtualenv ────────────────────────────────"
cd "$BACKEND_DIR"

PYTHON=$(command -v python3.11 2>/dev/null || command -v python3)
if [ ! -d "venv" ]; then
    echo "   Creating venv..."
    $PYTHON -m venv venv
fi
source venv/bin/activate
echo "✓  venv: $(which python)"

# ── 3. Install dependencies ───────────────────────────────────────────────────
echo ""
echo "── Installing dependencies ──────────────────────────"
pip install --upgrade pip -q
# Install base only — no Celery/Redis required for local dev
pip install -r requirements/base.txt -q
echo "✓  requirements/base.txt installed"

# ── 4. Environment file ───────────────────────────────────────────────────────
echo ""
echo "── Backend .env ─────────────────────────────────────"
if [ ! -f ".env" ]; then
    if [ -f ".env.local" ]; then
        cp .env.local .env
        echo "✓  Copied .env.local → .env"
    else
        echo "⚠  No .env or .env.local found. Creating minimal .env..."
        cat > .env << 'EOF'
SECRET_KEY=dev-secret-key-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=org_website
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
FRONTEND_URL=http://localhost:3000
CORS_ALLOWED_ORIGINS=http://localhost:3000
EMAIL_HOST=localhost
EMAIL_HOST_USER=dev
EMAIL_HOST_PASSWORD=dev
DEFAULT_FROM_EMAIL=dev@localhost
GOOGLE_CLIENT_ID=not-set
GOOGLE_CLIENT_SECRET=not-set
AWS_ACCESS_KEY_ID=not-set
AWS_SECRET_ACCESS_KEY=not-set
AWS_STORAGE_BUCKET_NAME=not-set
AWS_S3_REGION_NAME=us-east-1
EOF
        echo "✓  Created minimal .env"
    fi
else
    # Ensure POSTGRES_HOST is localhost in existing .env
    if grep -q "POSTGRES_HOST=db" .env; then
        sed -i.bak 's/POSTGRES_HOST=db/POSTGRES_HOST=localhost/' .env
        echo "✓  Fixed POSTGRES_HOST=db → localhost in .env"
    else
        echo "✓  .env already exists"
    fi
fi

# Unset any stale shell env that might override our .env
unset POSTGRES_HOST DB_HOST 2>/dev/null || true
export DJANGO_SETTINGS_MODULE=config.settings.development

# ── 5. Migrations ─────────────────────────────────────────────────────────────
echo ""
echo "── Migrations ───────────────────────────────────────"
python manage.py migrate --settings=config.settings.development
echo "✓  Migrations applied"

# ── 6. Frontend .env.local ────────────────────────────────────────────────────
echo ""
echo "── Frontend .env.local ──────────────────────────────"
if [ ! -f "$FRONTEND_DIR/.env.local" ]; then
    cat > "$FRONTEND_DIR/.env.local" << 'EOF'
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=local-dev-secret-replace-in-production-32chars
NEXT_PUBLIC_API_URL=http://localhost:8000
API_URL=http://localhost:8000
GOOGLE_CLIENT_ID=not-set
GOOGLE_CLIENT_SECRET=not-set
EOF
    echo "✓  Created frontend/.env.local"
else
    echo "✓  frontend/.env.local already exists"
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  ✅  Setup complete!                             ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "  Start backend:"
echo "    cd backend"
echo "    source venv/bin/activate"
echo "    DJANGO_SETTINGS_MODULE=config.settings.development python manage.py runserver"
echo ""
echo "  Start frontend (in another terminal):"
echo "    cd frontend && npm install && npm run dev"
echo ""
echo "  API docs: http://localhost:8000/api/schema/swagger-ui/"
echo ""
