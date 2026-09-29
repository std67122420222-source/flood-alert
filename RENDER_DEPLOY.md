# Deploy FloodAlert to Render

## 1) Push this project to GitHub

Create or use a GitHub repository and push the contents of this folder.
Do not upload `.env` or real API tokens.

## 2) Create a Web Service on Render

Render Dashboard → New → Web Service → connect the GitHub repository.

Recommended settings:

- Runtime: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 run:app`
- Health Check Path: `/healthz`
- Plan: Free

## 3) Environment Variables

Add:

- `SECRET_KEY` — generate a strong random value (Render can generate it for you)
- `TMD_ACCESS_TOKEN` — your new TMD Personal Access Token
- `TMD_WARNING_URL` — warning API URL used by the project

`DATABASE_URL` is optional for this demo. Without it the app uses SQLite.

## 4) Important Free-plan note

Render Free Web Services can spin down after 15 minutes of inactivity and their local filesystem is ephemeral. A local SQLite database can therefore be lost after redeploy/restart/spin-down. This is acceptable for a classroom/demo deployment, but not for persistent production data.

For persistent user accounts and tracked areas, migrate the database to PostgreSQL before treating the site as production.
