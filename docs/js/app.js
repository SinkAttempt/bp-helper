// BP Helper — Client-side data layer (localStorage)

const DB = {
    _get(key) {
        try { return JSON.parse(localStorage.getItem(key)) || []; }
        catch { return []; }
    },
    _set(key, data) {
        localStorage.setItem(key, JSON.stringify(data));
    },

    // BP Readings
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

    // Breathing Sessions
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
    if (systolic < 90 || diastolic < 60) return { cls: 'low', label: 'Low', color: '#3b82f6' };
    if (systolic < 120 && diastolic < 80) return { cls: 'normal', label: 'Normal', color: '#22c55e' };
    if (systolic < 130 && diastolic < 80) return { cls: 'elevated', label: 'Elevated', color: '#eab308' };
    if (systolic < 140 || diastolic < 90) return { cls: 'high1', label: 'High (Stage 1)', color: '#f97316' };
    return { cls: 'high2', label: 'High (Stage 2)', color: '#ef4444' };
}

// Flash messages
function showFlash(msg, type = 'success') {
    const el = document.getElementById('flash');
    if (!el) return;
    const colors = {
        success: 'bg-green-900/50 text-green-300 border-green-800',
        error: 'bg-red-900/50 text-red-300 border-red-800'
    };
    el.className = `mb-3 px-4 py-2 rounded-lg text-sm border ${colors[type] || colors.success}`;
    el.textContent = msg;
    el.classList.remove('hidden');
    setTimeout(() => el.classList.add('hidden'), 3000);
}

// Format date for display
function fmtDate(iso) {
    return iso ? iso.slice(0, 16).replace('T', ' ') : '';
}
function fmtDateShort(iso) {
    return iso ? iso.slice(0, 10) : '';
}
