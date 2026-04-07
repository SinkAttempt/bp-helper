# BP Helper: Current State

**Last updated:** 2026-04-07

## Status: MVP Complete (Not Deployed)

Working locally. Not yet deployed to Railway. No git repo initialised yet.

## What Works

1. **Dashboard** — shows average BP, 7-day trend chart (Chart.js), recent readings with AHA colour-coded categories, recent breathing sessions, quick-start breathing link
2. **BP Logging** — form with systolic/diastolic (required), pulse + notes (optional), input validation (range checks), AHA category classification on save
3. **Breathing Exercises** — 5 exercises available:
   - 4-7-8 Relaxing Breath (relaxation)
   - Box Breathing (focus)
   - Slow BP Breathing (BP reduction, 6 breaths/min)
   - Coherent Breathing 5-5 (HRV)
   - IMST Style (BP reduction)
4. **Breathing Timer** — animated circle (scale in/out), phase indicator (Breathe In/Hold/Breathe Out), countdown per phase, progress ring (SVG), cycle counter, auto-logs session on completion
5. **History** — full list of BP readings + breathing sessions with timestamps

## What's Missing (MVP scope — intentionally deferred)

- No auth (single user assumed)
- No PWA manifest
- No deployment config tested
- No git repo
- No tests
- No .env file created (using defaults)

## Files

```
bp-helper/
├── app.py                      — Flask entry, init_db on start
├── CLAUDE.md                   — Project instructions
├── .env.example                — Template
├── requirements.txt            — flask, gunicorn
├── runtime.txt                 — python-3.11.0
├── railway.json                — Railway deploy config
├── src/
│   ├── __init__.py
│   ├── config.py               — Env vars
│   ├── database.py             — SQLite CRUD
│   └── routes.py               — All routes + breathing exercise definitions
├── templates/
│   ├── base.html               — Layout, nav, Tailwind CDN
│   ├── dashboard.html          — Home with stats + chart
│   ├── log_bp.html             — BP entry form
│   ├── breathe_list.html       — Exercise picker
│   ├── breathe.html            — Timer with animations
│   └── history.html            — Full history
├── static/css/                 — (empty, using Tailwind CDN)
├── static/js/                  — (empty, JS inline in templates)
├── kb/subject/                 — Domain research
│   ├── breathing-science.md
│   ├── hypertension-stats.md
│   ├── competitor-analysis.md
│   └── breathnow-deep-dive.md
├── kb/project/                 — Project docs
│   ├── architecture.md
│   └── current-state.md        — This file
├── data/                       — SQLite DB (gitignored)
└── venv/                       — Python venv (gitignored)
```

## Known Issues

None yet — just built. Needs testing on actual mobile device.

## Origin

Inspired by analysis of BreathNow (Cardio Calm Ltd) app. George wanted a web-based, mobile-first alternative that leads with clinical evidence and has no App Store friction. See `kb/subject/breathnow-deep-dive.md` for full competitor analysis.
