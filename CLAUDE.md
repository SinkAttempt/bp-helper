# BP Helper

Blood pressure tracking + breathing exercise web app. Mobile-first MVP.

## Stack

Flask + Jinja + Tailwind CDN + SQLite (MVP) + Vanilla JS

## Run

```bash
python app.py
```

## Deploy

```bash
/opt/homebrew/bin/railway up
```

## Structure

```
app.py              — Flask entry point
src/config.py       — Env vars + validation
src/database.py     — SQLite helpers
src/routes.py       — All routes
templates/          — Jinja templates
static/css/         — Custom styles
static/js/          — Breathing timer + charts
kb/subject/         — Domain research (breathing, BP science, competitors)
kb/project/         — Project history, architecture, state
```

## Key Decisions

- SQLite for MVP (no external DB dependency), migrate to Postgres later
- Tailwind CDN (no build step)
- Session-based auth (no login for MVP — local use only)
- Mobile-first: designed for phone screens, works on desktop
