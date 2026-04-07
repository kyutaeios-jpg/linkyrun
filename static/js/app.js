'use strict';

/* ── Constants ─────────────────────────────────────────────── */
const STORAGE_KEY = 'namuSpeedrun';

/* ── State ─────────────────────────────────────────────────── */
let gameState = null;
let rafId     = null;

/* ── LocalStorage helpers ──────────────────────────────────── */
function loadState() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        return raw ? JSON.parse(raw) : null;
    } catch (_) { return null; }
}

function saveState(s) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
}

function clearState() {
    localStorage.removeItem(STORAGE_KEY);
}

/* ── Timer ─────────────────────────────────────────────────── */
function formatTime(ms) {
    const totalS = Math.floor(ms / 1000);
    const m  = Math.floor(totalS / 60);
    const s  = totalS % 60;
    const cs = Math.floor((ms % 1000) / 10);
    if (m > 0) {
        return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    }
    return `${String(s).padStart(2, '0')}.${String(cs).padStart(2, '0')}`;
}

function tickTimer() {
    if (!gameState || !gameState.active) return;
    const el = document.getElementById('timer-display');
    if (el) el.textContent = formatTime(Date.now() - gameState.startTime);
    rafId = requestAnimationFrame(tickTimer);
}

function stopTimer() {
    if (rafId !== null) {
        cancelAnimationFrame(rafId);
        rafId = null;
    }
}

/* ── HUD ────────────────────────────────────────────────────── */
function syncHUD() {
    const goalEl  = document.getElementById('goal-display');
    const hopsEl  = document.getElementById('hops-display');
    const timerEl = document.getElementById('timer-display');

    if (goalEl)  goalEl.textContent  = (gameState && gameState.goal)  || GOAL || '—';
    if (hopsEl)  hopsEl.textContent  = (gameState && gameState.hops != null) ? gameState.hops : '0';
    if (timerEl && !gameState?.active) {
        timerEl.textContent = gameState
            ? formatTime(Date.now() - gameState.startTime)
            : '00:00';
    }
}

/* ── Path panel ─────────────────────────────────────────────── */
function renderPath(path) {
    const el = document.getElementById('path-content');
    if (!el) return;
    if (!path || path.length === 0) {
        el.innerHTML = `<span class="path-empty">${t('pathEmpty')}</span>`;
        return;
    }
    el.innerHTML = path.map((p, i) => {
        const isCurrent = (i === path.length - 1);
        return [
            i > 0 ? '<span class="path-arrow">→</span>' : '',
            `<span class="path-item${isCurrent ? ' path-current' : ''}">${escapeHtml(p)}</span>`,
        ].join('');
    }).join('');
    el.scrollLeft = el.scrollWidth;
}

function togglePath() {
    const panel = document.getElementById('path-panel');
    if (!panel) return;
    panel.hidden = !panel.hidden;
    if (!panel.hidden) renderPath(gameState ? gameState.path : []);
}

/* ── Link filter ────────────────────────────────────────────── */
function filterLinks(query) {
    const cards   = document.querySelectorAll('.link-card');
    const q       = query.trim().toLowerCase();
    let   visible = 0;

    cards.forEach(card => {
        const title   = (card.dataset.title || '').toLowerCase();
        const display = card.textContent.trim().toLowerCase();
        const show    = !q || title.includes(q) || display.includes(q);
        card.style.display = show ? '' : 'none';
        if (show) visible++;
    });

    const countEl = document.getElementById('link-count');
    if (countEl) {
        const total = parseInt(countEl.dataset.total || cards.length, 10);
        countEl.textContent = q
            ? `${visible}/${total}${t('countUnit')}`
            : `${total}${t('countUnit')}`;
    }
}

/* ── Link click ─────────────────────────────────────────────── */
function handleLinkClick(title) {
    if (gameState && gameState.active) {
        gameState.hops++;
        gameState.path.push(title);
        saveState(gameState);
    }
}

/* ── Victory ────────────────────────────────────────────────── */
function showVictory() {
    stopTimer();

    const elapsed = gameState ? Date.now() - gameState.startTime : 0;

    if (gameState) {
        gameState.active  = false;
        gameState.elapsed = elapsed;
        saveState(gameState);
    }

    const timeEl = document.getElementById('victory-time');
    const hopsEl = document.getElementById('victory-hops');
    const pathEl = document.getElementById('victory-path');

    if (timeEl) timeEl.textContent = formatTime(elapsed);
    if (hopsEl) hopsEl.textContent = gameState ? `${gameState.hops}${t('hopsUnit')}` : '—';

    if (pathEl && gameState && gameState.path) {
        pathEl.innerHTML = gameState.path.map((p, i) => {
            const isGoal = (i === gameState.path.length - 1);
            return [
                i > 0 ? '<span class="vpath-arrow">→</span>' : '',
                `<span class="vpath-item${isGoal ? ' vpath-goal' : ''}">${escapeHtml(p)}</span>`,
            ].join('');
        }).join('');
    }

    const timerEl = document.getElementById('timer-display');
    if (timerEl) timerEl.textContent = formatTime(elapsed);

    // custom 게임은 랭킹 폼 숨김
    if (gameState && gameState.difficulty === 'custom') {
        const form = document.getElementById('ranking-form');
        if (form) form.style.display = 'none';
    }

    const overlay = document.getElementById('victory-overlay');
    if (overlay) overlay.hidden = false;
}

/* ── Actions ────────────────────────────────────────────────── */
function playAgain() {
    clearState();
    window.location.href = '/';
}

function giveUp() {
    if (!confirm(t('confirmGiveUp'))) return;
    clearState();
    window.location.href = '/';
}

async function submitRank() {
    if (!gameState) return;
    const nickname = document.getElementById('nickname-input').value.trim();
    if (!nickname) { alert(t('alertNoNick')); return; }

    const elapsed = gameState.elapsed || (Date.now() - gameState.startTime);
    const btn = document.getElementById('submit-rank-btn');
    btn.disabled = true;
    btn.textContent = t('submitting');

    try {
        const res = await fetch('/api/ranking', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nickname,
                start:      gameState.start,
                goal:       gameState.goal,
                elapsed_ms: Math.round(elapsed),
                hops:       gameState.hops,
                path:       gameState.path,
                difficulty: gameState.difficulty || 'unknown',
                wiki:       gameState.wiki || window._GAME_WIKI || 'ko',
                ...(gameState.dayNum ? { day_num: gameState.dayNum } : {}),
            }),
        });
        const data = await res.json();
        if (!data.ok) throw new Error(data.error || 'failed');

        const diff = gameState.difficulty || 'unknown';
        const rankRes  = await fetch(`/api/ranking?difficulty=${encodeURIComponent(diff)}&limit=50`);
        const rankData = await rankRes.json();
        const rank = rankData.rankings.findIndex(r => r.id === data.id) + 1;

        document.getElementById('ranking-input-row').hidden = true;
        const resultEl = document.getElementById('ranking-result');
        resultEl.hidden = false;
        resultEl.textContent = rank > 0 ? t('rankResult')(rank) : t('rankOk');
    } catch (e) {
        btn.disabled = false;
        btn.textContent = t('btnSubmitRank');
        alert(t('rankFail'));
    }
}

async function shareResult() {
    if (!gameState) return;
    const elapsed = gameState.elapsed || (Date.now() - gameState.startTime);
    const text = t('shareText')(gameState, formatTime(elapsed));

    if (navigator.share) {
        try { await navigator.share({ title: t('shareTitle'), text }); return; }
        catch (_) {}
    }
    try {
        await navigator.clipboard.writeText(text);
        alert(t('copied'));
    } catch (_) {
        alert(text);
    }
}

/* ── Util ───────────────────────────────────────────────────── */
function escapeHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

/* ── Init ───────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
    gameState = loadState();

    // Apply i18n (window._WIKI already set by inline script in page.html)
    if (typeof applyI18n === 'function') applyI18n();

    syncHUD();

    if (gameState && gameState.active && !IS_GOAL) {
        rafId = requestAnimationFrame(tickTimer);
    }

    if (IS_GOAL && gameState && gameState.active && gameState.hops > 0) {
        setTimeout(showVictory, 120);
    }

    // Wire up link cards
    document.querySelectorAll('.link-card').forEach(card => {
        const title = card.dataset.title;
        const goal  = card.dataset.goal;
        if (!title) return;

        card.href = `/page/${encodeURIComponent(title)}` +
                    (goal ? `?goal=${encodeURIComponent(goal)}` : '');

        card.addEventListener('click', () => handleLinkClick(title));
    });

    // Keyboard: / → focus search, Escape → clear search
    document.addEventListener('keydown', e => {
        if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
            e.preventDefault();
            const el = document.getElementById('link-filter');
            if (el) el.focus();
        }
        if (e.key === 'Escape') {
            const el = document.getElementById('link-filter');
            if (el && document.activeElement === el) {
                el.value = '';
                filterLinks('');
                el.blur();
            }
        }
    });
});
