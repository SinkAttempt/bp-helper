import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.database import (
    add_bp_reading, get_bp_readings, get_bp_stats, get_recent_trend,
    add_breathing_session, get_breathing_sessions
)

logger = logging.getLogger(__name__)
bp = Blueprint("main", __name__)

BREATHING_EXERCISES = {
    "4-7-8": {
        "name": "4-7-8 Relaxing Breath",
        "description": "Inhale 4s, hold 7s, exhale 8s. Developed by Dr. Andrew Weil. Activates parasympathetic nervous system.",
        "inhale": 4, "hold": 7, "exhale": 8, "cycles": 4,
        "category": "relaxation"
    },
    "box": {
        "name": "Box Breathing",
        "description": "Equal 4s phases: inhale, hold, exhale, hold. Used by Navy SEALs for stress control.",
        "inhale": 4, "hold": 4, "exhale": 4, "hold2": 4, "cycles": 6,
        "category": "focus"
    },
    "slow-bp": {
        "name": "Slow BP Breathing",
        "description": "6 breaths per minute. Clinically proven to lower blood pressure via baroreflex activation.",
        "inhale": 5, "hold": 0, "exhale": 5, "cycles": 6,
        "category": "bp-reduction"
    },
    "5-5": {
        "name": "Coherent Breathing",
        "description": "5s in, 5s out. Maximises heart rate variability. Simple and effective.",
        "inhale": 5, "hold": 0, "exhale": 5, "cycles": 10,
        "category": "hrv"
    },
    "imst": {
        "name": "IMST Style",
        "description": "Sharp inhale 5s with resistance, slow exhale 5s. Based on Inspiratory Muscle Strength Training research.",
        "inhale": 5, "hold": 2, "exhale": 5, "cycles": 6,
        "category": "bp-reduction"
    }
}


def classify_bp(systolic, diastolic):
    if systolic < 90 or diastolic < 60:
        return "low", "Low", "#3b82f6"
    elif systolic < 120 and diastolic < 80:
        return "normal", "Normal", "#22c55e"
    elif systolic < 130 and diastolic < 80:
        return "elevated", "Elevated", "#eab308"
    elif systolic < 140 or diastolic < 90:
        return "high1", "High (Stage 1)", "#f97316"
    elif systolic >= 140 or diastolic >= 90:
        return "high2", "High (Stage 2)", "#ef4444"
    else:
        return "crisis", "Crisis", "#dc2626"


@bp.route("/")
def dashboard():
    readings = get_bp_readings(limit=10)
    stats = get_bp_stats()
    trend = get_recent_trend(days=7)
    sessions = get_breathing_sessions(limit=5)

    classified_readings = []
    for r in readings:
        cls, label, color = classify_bp(r["systolic"], r["diastolic"])
        r["bp_class"] = cls
        r["bp_label"] = label
        r["bp_color"] = color
        classified_readings.append(r)

    return render_template("dashboard.html",
        readings=classified_readings,
        stats=stats,
        trend=trend,
        sessions=sessions,
        exercises=BREATHING_EXERCISES
    )


@bp.route("/log", methods=["GET", "POST"])
def log_bp():
    if request.method == "POST":
        try:
            systolic = int(request.form["systolic"])
            diastolic = int(request.form["diastolic"])
            pulse = request.form.get("pulse")
            pulse = int(pulse) if pulse else None
            notes = request.form.get("notes", "").strip() or None

            if not (40 <= systolic <= 300):
                flash("Systolic must be between 40-300", "error")
                return redirect(url_for("main.log_bp"))
            if not (20 <= diastolic <= 200):
                flash("Diastolic must be between 20-200", "error")
                return redirect(url_for("main.log_bp"))

            add_bp_reading(systolic, diastolic, pulse, notes)
            cls, label, _ = classify_bp(systolic, diastolic)
            flash(f"Logged {systolic}/{diastolic} — {label}", "success")
            return redirect(url_for("main.dashboard"))
        except (ValueError, KeyError) as e:
            logger.error(f"ERROR log_bp: {e}")
            flash("Invalid input", "error")
            return redirect(url_for("main.log_bp"))

    return render_template("log_bp.html")


@bp.route("/breathe")
def breathe_list():
    return render_template("breathe_list.html", exercises=BREATHING_EXERCISES)


@bp.route("/breathe/<exercise_id>")
def breathe(exercise_id):
    exercise = BREATHING_EXERCISES.get(exercise_id)
    if not exercise:
        flash("Unknown exercise", "error")
        return redirect(url_for("main.breathe_list"))
    return render_template("breathe.html", exercise=exercise, exercise_id=exercise_id)


@bp.route("/api/breathing-session", methods=["POST"])
def api_log_breathing():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    add_breathing_session(
        exercise_type=data.get("exercise_type", "unknown"),
        duration_seconds=data.get("duration_seconds", 0),
        pre_pulse=data.get("pre_pulse"),
        post_pulse=data.get("post_pulse")
    )
    return jsonify({"ok": True})


@bp.route("/history")
def history():
    readings = get_bp_readings(limit=100)
    classified = []
    for r in readings:
        cls, label, color = classify_bp(r["systolic"], r["diastolic"])
        r["bp_class"] = cls
        r["bp_label"] = label
        r["bp_color"] = color
        classified.append(r)
    sessions = get_breathing_sessions(limit=50)
    return render_template("history.html", readings=classified, sessions=sessions)


@bp.route("/api/trend")
def api_trend():
    days = request.args.get("days", 7, type=int)
    trend = get_recent_trend(days=days)
    return jsonify(trend)
