# CyberLearn (Full Stack)

CyberLearn is a full-stack web app with a SvelteKit frontend and Flask API backend.

## Project structure

- `frontend/` — SvelteKit + Bun + Tailwind UI
- `backend/` — Flask API server
- `database/schema.sql` — SQLite schema
- `database/seed.py` — seed/reset script for local data
- `vercel.json` — backend Vercel routing (`/api/*` -> `backend/vercel.py`)
- `.env.example` — shared env template (backend + frontend API config hints)

## Local development (full stack)

### Prerequisites

- Python 3.11+
- Bun 1.1+

### 1) Configure env

```bash
cp .env.example .env
```

### 2) Start backend (Flask)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python3 database/seed.py
python3 backend/run.py
```

Backend runs at `http://127.0.0.1:5000`.

### 3) Start frontend (SvelteKit)

In a new terminal:

```bash
cd frontend
bun install
bun run dev
```

Frontend runs at `http://127.0.0.1:5173`.

## Frontend API configuration

Frontend requests use `PUBLIC_API_BASE`.

- Default: `PUBLIC_API_BASE=/api`
- In local dev, Vite proxies `/api` to `BACKEND_DEV_ORIGIN` (default `http://127.0.0.1:5000`)
- To change proxy target locally, set `BACKEND_DEV_ORIGIN` before `bun run dev`
- To call a remote backend directly, set `PUBLIC_API_BASE` to a full URL (for example `https://my-api.vercel.app/api`)

For frontend-only env files, place values in `frontend/.env.local`.

## Seed workflow

`python3 database/seed.py`:

- creates database file if missing
- applies schema from `database/schema.sql`
- clears existing rows
- inserts sample users, tracks, modules, quizzes, and message history tables

Run it whenever you want a clean known dataset.

## API endpoints

All API routes are under `/api`:

- `GET /api/dashboard`
- `GET /api/tracks`
- `GET /api/tracks/<track_id>/modules`
- `GET /api/quizzes/<quiz_id>`
- `POST /api/quizzes/<quiz_id>/submit`
- `GET /api/progress`
- `POST /api/progress`
- `POST /api/analyze-message`
- `GET /api/message-history?limit=20`

## Gemini configuration and behavior

Backend-only env vars:

- `GEMINI_API_KEY` (required for analysis endpoint)
- `GEMINI_MODEL` (default: `gemini-1.5-flash`)

Behavior:

- Gemini is called only by backend code (`backend/app/services/gemini_service.py`)
- frontend never receives or stores Gemini credentials
- model output is normalized into strict response fields:
  - `verdict`
  - `riskLevel`
  - `redFlags`
  - `explanation`
  - `tips`

## CORS configuration for split frontend/backend deployments

Set backend `CORS_ORIGINS` to a comma-separated list of exact allowed frontend origins, for example:

```bash
CORS_ORIGINS=https://cyberlearn-frontend.vercel.app,http://localhost:5173
```

Notes:

- CORS is **not** open by default
- wildcard `*` is ignored by config parser
- only listed origins receive CORS headers for `/api/*`

## Deploying to Vercel (recommended: two projects)

Use one repo with two Vercel projects:

1. **Backend project**
   - Root Directory: `/` (repo root)
   - Uses `vercel.json` and deploys Flask from `backend/vercel.py`
   - Set env vars:
     - `DATABASE_PATH`
     - `DEFAULT_USER_ID`
     - `GEMINI_API_KEY`
     - `GEMINI_MODEL`
     - `CORS_ORIGINS` (include frontend production URL)

2. **Frontend project**
   - Root Directory: `frontend`
   - Framework preset: SvelteKit (auto-detected)
   - Set env vars:
     - `PUBLIC_API_BASE=https://<your-backend-domain>/api`

This setup keeps API and UI deployments independent while allowing frontend to target backend explicitly in production.

## Validation commands (frontend)

```bash
cd frontend
bun run check
bun run lint
bun run test
bun run build
```
