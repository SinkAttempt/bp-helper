// BP Helper — Client-side data layer (localStorage)

const DB = {
    _get(key) {
        try { return JSON.parse(localStorage.getItem(key)) || []; }
        catch { return []; }
    },
    _set(key, data) {
        localStorage.setItem(key, JSON.stringify(data));
    },
    addReading(systolic, diastolic, pulse, notes) {
        const readings = this._get('bp_readings');
        readings.unshift({
            id: Date.now(),
            systolic: parseInt(systolic),
            diastolic: parseInt(diastolic),
            pulse: pulse ? parseInt(pulse) : null,
            notes: notes || null,
            created_at: new Date().toISOString()
        });
        this._set('bp_readings', readings);
    },
    getReadings(limit = 100) {
        return this._get('bp_readings').slice(0, limit);
    },
    getStats() {
        const readings = this._get('bp_readings');
        if (!readings.length) return null;
        const avg = (arr) => Math.round(arr.reduce((a, b) => a + b, 0) / arr.length);
        const pulses = readings.filter(r => r.pulse).map(r => r.pulse);
        return {
            total: readings.length,
            avg_systolic: avg(readings.map(r => r.systolic)),
            avg_diastolic: avg(readings.map(r => r.diastolic)),
            avg_pulse: pulses.length ? avg(pulses) : null,
            min_systolic: Math.min(...readings.map(r => r.systolic)),
            max_systolic: Math.max(...readings.map(r => r.systolic))
        };
    },
    getTrend(days = 7) {
        const readings = this._get('bp_readings');
        const cutoff = new Date();
        cutoff.setDate(cutoff.getDate() - days);
        const byDate = {};
        for (const r of readings) {
            const d = new Date(r.created_at);
            if (d < cutoff) continue;
            const key = d.toISOString().slice(0, 10);
            if (!byDate[key]) byDate[key] = [];
            byDate[key].push(r);
        }
        return Object.entries(byDate)
            .sort(([a], [b]) => a.localeCompare(b))
            .map(([date, rs]) => ({
                date,
                avg_systolic: Math.round(rs.reduce((s, r) => s + r.systolic, 0) / rs.length),
                avg_diastolic: Math.round(rs.reduce((s, r) => s + r.diastolic, 0) / rs.length),
                readings: rs.length
            }));
    },
    addSession(exerciseType, durationSeconds) {
        const sessions = this._get('breathing_sessions');
        sessions.unshift({
            id: Date.now(),
            exercise_type: exerciseType,
            duration_seconds: durationSeconds,
            created_at: new Date().toISOString()
        });
        this._set('breathing_sessions', sessions);
    },
    getSessions(limit = 50) {
        return this._get('breathing_sessions').slice(0, limit);
    }
};

// BP Classification (AHA 2017)
function classifyBP(systolic, diastolic) {
    if (systolic < 90 || diastolic < 60) return { cls: 'low', label: 'Low', color: '#3b82f6', bg: 'rgba(59,130,246,0.12)' };
    if (systolic < 120 && diastolic < 80) return { cls: 'normal', label: 'Normal', color: '#16a34a', bg: 'rgba(74,222,128,0.15)' };
    if (systolic < 130 && diastolic < 80) return { cls: 'elevated', label: 'Elevated', color: '#ca8a04', bg: 'rgba(250,204,21,0.15)' };
    if (systolic < 140 || diastolic < 90) return { cls: 'high1', label: 'High (Stage 1)', color: '#ea580c', bg: 'rgba(251,146,60,0.15)' };
    return { cls: 'high2', label: 'High (Stage 2)', color: '#dc2626', bg: 'rgba(248,113,113,0.15)' };
}

function showFlash(msg, type = 'success') {
    const el = document.getElementById('flash');
    if (!el) return;
    el.className = `flash flash-${type}`;
    el.textContent = msg;
    el.style.display = 'block';
    setTimeout(() => el.style.display = 'none', 3000);
}

function fmtDate(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' }) + ' ' + d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
}
function fmtDateShort(iso) {
    if (!iso) return '';
    return new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
}

// Week strip
function renderWeekStrip() {
    const today = new Date();
    const dow = today.getDay();
    const monday = new Date(today);
    monday.setDate(today.getDate() - ((dow + 6) % 7));
    const days = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
    const readings = DB.getReadings(200);
    const readingDates = new Set(readings.map(r => r.created_at.slice(0, 10)));

    let html = '';
    for (let i = 0; i < 7; i++) {
        const d = new Date(monday);
        d.setDate(monday.getDate() + i);
        const dateStr = d.toISOString().slice(0, 10);
        const isToday = dateStr === today.toISOString().slice(0, 10);
        const hasReading = readingDates.has(dateStr);
        html += `<div class="week-day${isToday ? ' active' : ''}${hasReading ? ' has-reading' : ''}">
            <span class="label">${days[i]}</span>
            <span class="date">${d.getDate()}</span>
        </div>`;
    }
    return html;
}

// BP progress ring SVG
function bpRingSVG(systolic, target = 120) {
    const pct = Math.min(systolic / 180, 1);
    const circ = 2 * Math.PI * 48;
    const offset = circ * (1 - pct);
    const bp = classifyBP(systolic, 80);
    return `<div class="progress-ring-wrap">
        <svg viewBox="0 0 120 120">
            <circle class="progress-ring-bg" cx="60" cy="60" r="48"/>
            <circle class="progress-ring-fill" cx="60" cy="60" r="48"
                stroke="${bp.color}" stroke-dasharray="${circ}" stroke-dashoffset="${offset}"/>
        </svg>
        <div class="progress-ring-text">
            <span class="value">${systolic}</span>
            <span class="label">mmHg</span>
        </div>
    </div>`;
}
