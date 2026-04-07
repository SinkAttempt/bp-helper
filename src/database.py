import sqlite3
import os
import logging
from contextlib import contextmanager
from src.config import DATABASE_PATH

logger = logging.getLogger(__name__)


def init_db():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    logger.info(f"STARTUP init_db: {DATABASE_PATH}")
    with get_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS bp_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                systolic INTEGER NOT NULL,
                diastolic INTEGER NOT NULL,
                pulse INTEGER,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS breathing_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exercise_type TEXT NOT NULL,
                duration_seconds INTEGER NOT NULL,
                pre_pulse INTEGER,
                post_pulse INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    logger.info("STARTUP init_db: tables ready")


@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def add_bp_reading(systolic, diastolic, pulse=None, notes=None):
    logger.info(f"DB add_bp_reading: {systolic}/{diastolic} pulse={pulse}")
    with get_db() as db:
        db.execute(
            "INSERT INTO bp_readings (systolic, diastolic, pulse, notes) VALUES (?, ?, ?, ?)",
            (systolic, diastolic, pulse, notes)
        )


def get_bp_readings(limit=50):
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM bp_readings ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_bp_stats():
    with get_db() as db:
        row = db.execute("""
            SELECT
                COUNT(*) as total,
                ROUND(AVG(systolic), 1) as avg_systolic,
                ROUND(AVG(diastolic), 1) as avg_diastolic,
                ROUND(AVG(pulse), 1) as avg_pulse,
                MIN(systolic) as min_systolic,
                MAX(systolic) as max_systolic
            FROM bp_readings
        """).fetchone()
    return dict(row) if row else {}


def get_recent_trend(days=7):
    with get_db() as db:
        rows = db.execute("""
            SELECT
                DATE(created_at) as date,
                ROUND(AVG(systolic), 1) as avg_systolic,
                ROUND(AVG(diastolic), 1) as avg_diastolic,
                COUNT(*) as readings
            FROM bp_readings
            WHERE created_at >= DATE('now', ?)
            GROUP BY DATE(created_at)
            ORDER BY date
        """, (f"-{days} days",)).fetchall()
    return [dict(r) for r in rows]


def add_breathing_session(exercise_type, duration_seconds, pre_pulse=None, post_pulse=None):
    logger.info(f"DB add_breathing_session: {exercise_type} {duration_seconds}s")
    with get_db() as db:
        db.execute(
            "INSERT INTO breathing_sessions (exercise_type, duration_seconds, pre_pulse, post_pulse) VALUES (?, ?, ?, ?)",
            (exercise_type, duration_seconds, pre_pulse, post_pulse)
        )


def get_breathing_sessions(limit=20):
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM breathing_sessions ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]
