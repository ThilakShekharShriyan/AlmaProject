# Lead intake

Public prospect form, attorney review, and email notification. Five processes on the host. No Docker in this pass.

## What you need

- Python 3.12
- Node.js 20+
- Local Postgres, Redis, and Mailpit

On macOS:

```bash
brew install python@3.12 postgresql@16 redis mailpit
brew services start postgresql@16
brew services start redis
brew services start mailpit
```

Create the three databases once. `psql` is under the Postgres keg if it is not on your PATH.

```bash
PSQL=/opt/homebrew/opt/postgresql@16/bin/psql
$PSQL -d postgres -c "CREATE DATABASE identity_db"
$PSQL -d postgres -c "CREATE DATABASE documents_db"
$PSQL -d postgres -c "CREATE DATABASE leads_db"
```

## Configure

```bash
cp .env.example .env
python3.12 -m venv .venv
.venv/bin/pip install -U pip
.venv/bin/pip install \
  'fastapi>=0.115' 'uvicorn>=0.32' 'sqlalchemy>=2.0' 'psycopg[binary]>=3.2' \
  'pydantic-settings>=2.6' 'pydantic[email]>=2.6' 'bcrypt>=4' 'pyjwt>=2.9' \
  'redis>=5' 'python-multipart' 'alembic>=1.13' 'pytest>=8' 'httpx>=0.27'
```

Each service uses the package name `app`, so do not install them into one environment. Run a service with `--app-dir`, and run its tests from that service directory.

Seeded attorney, from `.env.example` until you change `.env`:

- email `attorney@example.com`
- password `change-me`

Mailpit inbox: http://localhost:8025

## Run

From the repo root, in separate terminals:

```bash
set -a && source .env && set +a
.venv/bin/uvicorn app.main:app --app-dir apps/identity --port 8001
.venv/bin/uvicorn app.main:app --app-dir apps/documents --port 8002
.venv/bin/uvicorn app.main:app --app-dir apps/leads --port 8003
.venv/bin/uvicorn app.main:app --app-dir apps/notifications --port 8004
```

```bash
cd apps/web
npm install
npm run dev
```

Open http://localhost:3000/apply

## Tests

```bash
(cd apps/identity && ../../.venv/bin/pytest -q)
(cd apps/documents && ../../.venv/bin/pytest -q)
(cd apps/leads && ../../.venv/bin/pytest -q)
(cd apps/notifications && ../../.venv/bin/pytest -q)
```

## Demo path

1. Submit the public form with a PDF resume.
2. Open Mailpit and confirm mail to the prospect and the attorney.
3. Sign in at `/login`.
4. Open the lead, download the resume, and click Reach out. Status becomes `REACHED_OUT`.
