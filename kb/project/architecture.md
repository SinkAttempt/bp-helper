# BP Helper: Architecture & Tech Decisions

## Overview

BP Helper is a mobile-first web application for tracking blood pressure and practicing clinically-proven breathing exercises. Built as an MVP to validate the concept before investing in native app development.

## Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Backend | Flask 3.1 | Simple, George's standard, sufficient for MVP |
| Templates | Jinja2 | Server-rendered, no build step, fast iteration |
| CSS | Tailwind CDN | Mobile-first utility classes, no build step |
| JS | Vanilla | Breathing timer only needs simple DOM manipulation |
| Charts | Chart.js 4 (CDN) | Lightweight, good mobile touch support |
| Database | SQLite | Zero-config for MVP, file-based, migrate to Postgres for prod |
| Hosting | Railway | George's standard personal deployment |
| Runtime | Python 3.11 | Stable, avoids 3.13 httpx issues |

## Architecture

```
Request → Flask → Blueprint routes → SQLite
                      ↓
              Jinja2 templates → Tailwind CSS
                      ↓
              Client-side JS (breathing timer, charts)
```

No API-first architecture. Server-rendered pages with sprinkles of JS where needed (breathing timer, trend charts). Progressive enhancement — works without JS except for breathing exercises.

## Database Schema

### bp_readings
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| systolic | INTEGER NOT NULL | 40-300 validated |
| diastolic | INTEGER NOT NULL | 20-200 validated |
| pulse | INTEGER | Optional |
| notes | TEXT | Optional free text |
| created_at | TIMESTAMP | Default CURRENT_TIMESTAMP |

### breathing_sessions
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| exercise_type | TEXT NOT NULL | Exercise name |
| duration_seconds | INTEGER NOT NULL | Actual session length |
| pre_pulse | INTEGER | Optional: pulse before |
| post_pulse | INTEGER | Optional: pulse after |
| created_at | TIMESTAMP | Default CURRENT_TIMESTAMP |

## Key Design Decisions

### Why web, not native?
1. **No App Store friction** — instant access via URL
2. **Faster iteration** — deploy in seconds vs app review
3. **Cross-platform free** — works on any phone browser
4. **PWA potential** — can add to home screen later
5. **Validates demand** before investing in Swift/Kotlin

### Why SQLite for MVP?
1. Zero external dependencies
2. File-based = easy backup
3. Sufficient for single-user / low-traffic MVP
4. Migration path to Postgres is straightforward (same SQL patterns)

### Why no auth for MVP?
1. Personal use / demo only initially
2. Reduces complexity
3. Auth adds friction for trying the product
4. Can add session-based auth or OAuth later

### Why dark theme?
1. Most health apps use dark themes (Calm, Fitbit, Apple Health)
2. Reduces eye strain for evening use (when many people check BP)
3. OLED battery savings on mobile
4. Looks more premium

## Feature Priority (MVP vs Later)

### MVP (Current)
- [x] Manual BP logging with validation
- [x] BP classification (AHA categories)
- [x] 5 breathing exercises with animated timer
- [x] Session tracking (auto-logged on completion)
- [x] 7-day trend chart
- [x] History view
- [x] Mobile-first responsive UI
- [x] Bottom navigation (app-like feel)

### Phase 2 (Next)
- [ ] PWA manifest + service worker (offline, install)
- [ ] User accounts (email/password or magic link)
- [ ] Export to PDF/CSV (for doctor visits)
- [ ] Reminders (push notifications via PWA)
- [ ] Before/after pulse tracking per session
- [ ] Time-of-day analysis (morning vs evening)

### Phase 3 (Later)
- [ ] Telegram bot companion
- [ ] AI insights (trend analysis, recommendations)
- [ ] Bluetooth BP monitor integration (Web Bluetooth API)
- [ ] Social features (anonymous progress sharing)
- [ ] Apple Health / Google Fit sync
- [ ] Premium tier (advanced analytics, personalised plans)

## URL Structure

| Route | Purpose |
|-------|---------|
| / | Dashboard (stats, recent readings, quick breathe) |
| /log | Log new BP reading |
| /breathe | Exercise list |
| /breathe/<id> | Individual breathing exercise timer |
| /history | Full history of readings + sessions |
| /api/breathing-session | POST: log completed session |
| /api/trend | GET: trend data (JSON) |
