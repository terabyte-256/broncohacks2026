# AGENTS.md

This file provides essential guidance for OpenCode agents working in this repository to avoid common mistakes and ramp up quickly.

## Database & Backend
- **Database location**: `/database/cyberlearn.db` (SQLite)
- **Schema file**: `/database/schema.sql` - contains all table definitions
- **Seed data**: Run `python3 database/seed.py` to reset and populate test data
- **Backend entrypoint**: `backend/run.py` - starts Flask app on port 5000 by default
- **Virtual environment**: Backend uses venv - activate with `source backend/venv/bin/activate`
- **Dependencies**: Install with `pip install -r backend/requirements.txt`
- **Port conflicts**: If port 5000 is in use, set `PORT=5001` when starting backend
- **API proxy**: Frontend Vite config proxies `/api` to backend (default: http://127.0.0.1:5000)

## OAuth Login (Google)
- **Setup**: Requires `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` environment variables
- **Routes**:
  - `GET /auth/login` - Initiates OAuth flow
  - `GET /auth/login/callback` - Handles OAuth callback
  - `GET /auth/user` - Returns current user JSON (requires session)
  - `GET /auth/logout` - Clears session
- **Session**: Stores `user_id`, `user_name`, `user_email` after successful login
- **Database**: Users table includes `oauth_provider` and `oauth_id` fields
- **Implementation**: Logic in `/backend/app/routes/auth.py`

## Analytics Endpoint
- **Endpoint**: `GET /api/analytics` (under dashboard blueprint)
- **Returns JSON**:
  ```json
  {
    "total_users": 42,
    "total_quiz_attempts": 128,
    "average_score": 78.5,
    "completed_topics": 15,
    "attempts_per_track": [
      {"track": "Web Development", "count": 45},
      {"track": "Data Science", "count": 32}
    ]
  }
  ```
- **Service**: Logic in `/backend/app/services/analytics_service.py`
- **Queries**: Uses SQLite to compute user stats, quiz attempts, average scores, completed topics, and track-based attempts

## Analytics Frontend
- **Page**: Svelte route at `/analytics`
- **Features**:
  - Metric cards showing total users, quiz attempts, average score, completed topics
  - Bar chart of quiz attempts per track using Chart.js
- **Component**: Located at `/frontend/src/routes/analytics/+page.svelte`
- **Chart**: Uses Chart.js library (installed via `npm install chart.js`)
- **Navigation**: Link added to global layout (`/+layout.svelte`)

## Development Workflow
1. **Database**: Run `python3 database/seed.py` to initialize test data
2. **Backend**: 
   - `cd backend && source venv/bin/activate`
   - `PORT=5001 python3 run.py` (or default 5000 if available)
3. **Frontend**: `cd frontend && npm run dev`
4. **Access**: 
   - Home page: http://localhost:5173
   - Analytics: http://localhost:5173/analytics
   - OAuth login: http://localhost:5173/auth/login (proxied to backend)
   - API docs: http://localhost:5001/api/analytics

## Environment Variables
- **Backend**: 
  - `DATABASE_PATH` (defaults to `/database/cyberlearn.db`)
  - `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` (for OAuth)
  - `GEMINI_API_KEY` (for AI features)
  - `DEFAULT_USER_ID` (defaults to 1)
  - `PORT` (defaults to 5000)
- **Frontend**:
  - `BACKEND_DEV_ORIGIN` (defaults to `http://127.0.0.1:5000`)

## Testing
- To test OAuth: Navigate to `/auth/login` in frontend (will proxy to backend)
- To test analytics: Visit `/analytics` page or call `/api/analytics` directly
- Ensure backend is running before testing frontend features
- Check logs: `backend/backend.log` and `frontend/frontend.log` for debugging
